# airport
The main program is in main.py

All airports in the USA is in usa_airports.csv

To start scraping:
- download this repository
- navigate to the root folder `airport/`
- run `python main.py`
- Input your task csv number, 0, 1, 2 or 3
- Input the date
- the result will be write to `csv/results.csv`

About running time:
- a flight search between two city usually takes about 0.1 seconds
- one piece of task has more than 30k searches, which takes about 1 hour to finish or more
- In total, 4 hours are estimated to finish scraping 400 major airports in USA.
-