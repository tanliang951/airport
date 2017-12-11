# airport
The main program is in main.py

All airports in the USA is in usa_airports.csv

To start scraping:
- download this repository
- navigate to the root folder `airport/`
- run `python main.py`
- Input the full path to task file (specifying arrv, dept in every row) as indicated
- Input the date
- the result will be write to `csv/results.csv`

About running time:
- a flight search between two city usually takes about 0.1 seconds
- one piece of task has more than 30k searches, which takes about 1 hour to finish or more
- In total, 4 hours are estimated to finish scraping 400 major airports in USA.

Make sure you have the following libraries:
- Beautifulsoup
- requests
- pandas

About requests `ConnectionError`
- The reason for this error is unknown
- Try-catch in code now. It simply skips this search and return an empty list. Then print the information in output. To record the skip information, pipe the output to a file so later you can redo the missing requests mannually
- Run code like this
`python main.py > log.txt`
