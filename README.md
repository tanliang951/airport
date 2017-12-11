__This is the windows version__

create a virtualenv for project packages
```sh
pip install virtualenv
cd Desktop\
virtualenv airport
cd airports\
# activate the virtual env
\Scripts\activate
```
After this, `airport` will prefix your command prompt. It means that a new python environment is created to store your
new packages. It avoids conflicts with your global python envrionment.

Install dependencies using pip
```sh
pip install requests
pip install bs4
pip install pandas
pip install lxml # this seems necessary or bs cannot parse the document tree
```

Others run as usual.

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

No happy coding!
