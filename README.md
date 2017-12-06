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

pyplpr is meant to be easily extensible with new "providers" of information about local names and holidays and with new output formats.

Launch the script with the `-h` command line argument to get a list of the available options.

At the moment, the script has been tested to work on Linux with Python 3.5 or higher.

Supported output formats and options
------------------------------------

- **html** (default): full-width HTML page
  - **extstyle**: if specified, replace embedded CSS with a link to a named file
- **ascii**: ASCII characters-based table
  - **colwidth**: characters per column
