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
    print('<!DOCTYPE html', file=out)
    print('<html lang="en">', file=out)
    print('<title>Planner</title>', file=out)
    print('<link rel="stylesheet" type="text/css", href="style.css">', file=out)
    print('</head>', file=out)
    print('<body>', file=out)
    print('<table class="p3table">', file=out)
    print('<tr class="p3header">', file=out)
    for month in data["monthnames"]:
        print('<td>{}</td>'.format(month), file=out)
    print('</tr>', file=out)
    for day in range(31):
        print('<tr class="p3dayrow">', file=out)
        for month in range(12):
            if day < data["daycount"][month]:
                print('<td class="p3day">{}{:2}</td>'.format(data["downames"][(data["firstdow"][month] + day) % 7][0].upper(), day+1), file=out)
            else:
                print('<td class="p3empty"></td>', file=out)
        print('</tr>', file=out)
    print('</table>', file=out)
    print('</body>', file=out)
    print('</html>', file=out)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("year", type=int, default=None, nargs="?",
                        help="calendar year (default: year of next month)")
    parser.add_argument("-l", "--locale",
                        help="calendar locale (default: system locale)")
    args = parser.parse_args()
    if not args.year:
        from datetime import date, timedelta
        args.year = (date.today() + timedelta(days=31)).year
    data = make_data(args.year, args.locale)
    with open("test.html", "wt") as output:
        renderer_html(output, data)
