default_providers = {
    "monthnames": "python",
    "downames": "python"
}

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
    from urllib import request
    import json
    url = "http://kayaposoft.com/enrico/json/v1.0/?action=getPublicHolidaysForYear&year={}&country={}&region=" \
            .format(year, country)
    with request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    return {(h["date"]["month"], h["date"]["day"]): h["localName"]
            for h in data}

def locate_provider(key, name):
    return globals()["provider_{}_{}".format(key, name)]

def make_data(year, country=None, providers={}):
    from datetime import date
    providers = providers.copy()
    providers.update(default_providers)
    if not country:
        import locale
        country, _ = locale.getdefaultlocale()
    data = {key: locate_provider(key, prov)(country)
            for key, prov in providers.items()}
    leap = year%4 == 0 and (year%100 != 0 or year%400 == 0)
    data["daycount"] = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    data["firstdow"] = [date(year, month, 1).weekday() for month in range(1, 13)]
    return data

def renderer_html(out, data):
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader(__name__, 'templates'))
    template = env.get_template("template.html")
    template.stream(data).dump(out)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("year", type=int, default=None, nargs="?",
                        help="calendar year (default: year of next month)")
    parser.add_argument("-l", "--locale",
                        help="calendar locale (default: system locale)")
    parser.add_argument("-n", "--holidays",
                        help="include holidays of specified nation")
    parser.add_argument("-o", "--output",
                        help="name of output file (default: standard output)")
    args = parser.parse_args()
    if not args.year:
        from datetime import date, timedelta
        args.year = (date.today() + timedelta(days=31)).year
    data = make_data(args.year, args.locale)
    if args.holidays:
        data["holidays"] = provider_holidays_enrico(args.holidays, args.year)
    if args.output:
        with open(args.output, "wt") as output:
            renderer_html(output, data)
    else:
        import sys
        renderer_html(sys.stdout, data)
