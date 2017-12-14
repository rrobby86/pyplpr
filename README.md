*(work in progress)*

**pyplpr** (*Python Planner Printer*) is a small script to generate yearly planner calendars ready to be printed, providing a (small) space to take notes in each day. The output resembles the following:

| January | February | March | ... |
| ------- | -------- | ----- | --- |
| M 1     | T 1      | T 1   | ... |
| T 2     | F 2      | F 2   | ... |
| W 3     | S 3      | S 3   | ... |
| T 4     | S 4      | S 4   | ... |
| ...     | ...      | ...   | ... |

Names of months and days of week are obtained from the `locale` module in Python. Dates and names of national holidays (if requested) are retrieved from [Enrico Service](http://kayaposoft.com/enrico/).

pyplpr is meant to be easily extensible with new "providers" of information about local names and holidays and with new output formats. Output for included formats is produced using the [Jinja2](http://jinja.pocoo.org/) template engine.

Launch the script with the `-h` command line argument to get a list of the available options.

At the moment, the script has been tested to work on Linux with Python 2.7 or 3.5+ and requires to manually install Jinja2 (`pip install Jinja2`).

Command line options
--------------------

Use the `-h` option to print the list of available options.

You can specify the calendar year as an argument; if not specified, the next year is assumed if current month is December, the current year is assumed otherwise.

- `-l`: explicitly set the locale for names of months and days of week, e.g. `-l it` or `-l en_US`, it must be installed in the system
- `-n`: specify 3-letters code of country for which national holidays must be included, e.g. `-l ita` or `-l usa`
- `-f`: set the output format, default is `html`, see supported formats below
- `-s`: set options for the used format, e.g. `extstyle=planner.css`, see below
- `-o`: set name of output file, standard output is used if not given

Supported output formats and options
------------------------------------

- **html** (default): full-width HTML page
  - **extstyle**: if specified, replace embedded CSS with a link to a named file
- **ascii**: ASCII characters-based table
  - **colwidth**: characters per column
- **latex**: LaTeX source file of landscape A3 page *(requires pdflatex to generate a usable PDF)*
