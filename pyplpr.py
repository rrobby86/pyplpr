default_providers = {
    "monthnames": "python",
    "downames": "python"
}

def urlopen(*args, **kwargs):
    if "_urlopen" not in globals():
        global _urlopen
        try:
            from urllib.request import urlopen
            dourlopen = urlopen
        except ImportError:
            from urllib import urlopen
            from contextlib import closing
            def dourlopen(*args, **kwargs):
                return closing(urlopen(*args, **kwargs))
        _urlopen = dourlopen
    return _urlopen(*args, **kwargs)

def provider_monthnames_python(country):
    import locale
    locale.setlocale(locale.LC_ALL, (country, "UTF-8"))
    return [locale.nl_langinfo(getattr(locale, "MON_" + str(i)))
            for i in range(1, 13)]

def provider_downames_python(country):
    import locale
    locale.setlocale(locale.LC_ALL, (country, "UTF-8"))
    return [locale.nl_langinfo(getattr(locale, "DAY_" + str(i%7+1)))
            for i in range(1, 8)]

def provider_holidays_enrico(country, year):
    import json
    url = "http://kayaposoft.com/enrico/json/v1.0/" \
            "?action=getPublicHolidaysForYear&year={}&country={}&region=" \
            .format(year, country)
    with urlopen(url) as url:
        data = json.loads(url.read().decode())
    return {(h["date"]["month"], h["date"]["day"]): h["localName"]
            for h in data}

def locate_provider(key, name):
    return globals()["{}_{}".format(key, name)]

def make_data(year, country=None, providers={}):
    from datetime import date
    providers = providers.copy()
    providers.update(default_providers)
    if not country:
        import locale
        country, _ = locale.getdefaultlocale()
    data = {key: locate_provider("provider_" + key, prov)(country)
            for key, prov in providers.items()}
    leap = year%4 == 0 and (year%100 != 0 or year%400 == 0)
    data["daycount"] = [31, 29 if leap else 28, 31, 30, 31, 30,
                        31, 31, 30, 31, 30, 31]
    data["firstdow"] = [date(year, month, 1).weekday()
                        for month in range(1, 13)]
    return data

def jinja_renderer(template_file, default_opts={}, **env_options):
    def result(out, data, **options):
        from jinja2 import Environment, PackageLoader
        env = Environment(loader=PackageLoader(__name__, "templates"),
                **env_options)
        template = env.get_template(template_file)
        for key, val in default_opts.items():
            if key in options:
                val = type(val)(options.pop(key))
            data[key] = val
        if options:
            if len(options) <= 3:
                raise Exception("Unrecognized style options: " +
                                ", ".join(options.keys()))
            else:
                raise Exception("{} unrecognized style options"
                                .format(len(options)))
        from sys import version_info
        if version_info.major >= 3:
            template.stream(data).dump(out) # fails in py2
        else:
            out.write(template.render(data, encoding="utf-8"))
    return result

renderer_html = jinja_renderer("template.html", {"extstyle": ""},
                               trim_blocks=True)

renderer_ascii = jinja_renderer("ascii.txt", {"colwidth": 16},
                                trim_blocks=True)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("year", type=int, default=None, nargs="?",
                        help="calendar year (default: year of next month)")
    parser.add_argument("-l", "--locale",
                        help="calendar locale (default: system locale)")
    parser.add_argument("-n", "--holidays", metavar="country",
                        help="include holidays of country with specified ISO" \
                        " 3166-1 alpha-3 code")
    parser.add_argument("-f", "--format", default="html",
                        help="output format (default: html)")
    parser.add_argument("-s", "--style", action="append", metavar="opts",
                        help="comma-separated format-specific options")
    parser.add_argument("-o", "--output", metavar="file",
                        help="name of output file (default: standard output)")
    args = parser.parse_args()
    if not args.year:
        from datetime import date, timedelta
        args.year = (date.today() + timedelta(days=31)).year
    data = make_data(args.year, args.locale)
    if args.holidays:
        data["holidays"] = provider_holidays_enrico(args.holidays, args.year)
    renderer = locate_provider("renderer", args.format)
    format_opts = {}
    if args.style:
        import re
        from shlex import shlex
        re_opt = re.compile("([a-zA-z_][a-zA-Z_0-9]*)(?:=(.+))?")
        for s in args.style:
            lexer = shlex(s, posix=True)
            lexer.whitespace_split = True
            lexer.whitespace = ","
            for opt in lexer:
                key, val = re_opt.fullmatch(opt).groups()
                format_opts[key] = val if val is not None else True
    if args.output:
        from io import open
        with open(args.output, "wt", encoding="utf-8") as output:
            renderer(output, data, **format_opts)
    else:
        import sys
        renderer(sys.stdout, data, **format_opts)
