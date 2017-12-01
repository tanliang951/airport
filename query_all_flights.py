#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 05:21:13 2017

@author: RockyYeung
"""

"""
date: 12/01/2017
from: LAS
to: DCA
"""
import sys
import bs4 as bs
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage

"""
12/01/2017
"""

from_ = "AAF"
to = "ABE"
date = "12/01/2017"

# add maxhop to query only non-stop
url_temp = "https://www.orbitz.com/Flights-Search?trip=oneway&leg1=from:{from_},to:{to},\
departure:{date}TANYT&passengers=children:0,adults:1,seniors:0,\
infantinlap:Y&options=maxhops%3A0&mode=search"


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


url = url_temp.format(from_=from_, to=to, date=date)
page = Page(url)
soup = bs.BeautifulSoup(page.html, 'html.parser')
ul = soup.find('ul', {'id': "flightModuleList"})
flights = ul.find_all('li', class_="flight-module")

def process_flight(f):
    try:
        dept_time = f.find("span", {"class": "departure-time departure-0-emphasis",
                            "data-test-id": "departure-time"}).text.strip()
        arrv_time = f.find("span", {"class": "arrival-time arrival-0-emphasis",
                                "data-test-id": "arrival-time"}).text.strip()
        duration = f.find("div", {"class": "primary duration-emphasis",
                                  "data-test-id": "duration"}).text.strip()
        # LAX - DCA
        airport_from, airport_to = f.find("div", {"class": "secondary", "data-test-id": "airports"}).text.strip().split(" - ")
        airline_name = f.find("div", {"class": "secondary truncate", 
                                      "data-test-id": "airline-name"}).text.strip()
        # American Airlines 52, dynamically loaded
        flight_number = f.find("dd", {"class": "flight", 
                                      "data-test-id": "details-airline-data"}).text.strip()
#        # 2,295 mi
#        distance = f.find("dd", {"class": "details-utility-item-value"}).text.strip()
#        class_type = f.find("dd", {"data-test-id": "details-class-type"}).text.strip()
#        aircraft = f.find("dd", {"class": "aircraft"}).text.strip()
        
    except AttributeError:
        raise Exception("fields are not complete")
    
    return {"dept_time": dept_time, "arrv_time": arrv_time, 
            "duration": duration, "airline-name": airline_name,
            "airport_from": airport_from, "airport_to": airport_to}
#            "flight_number": flight_number, "distance": distance,
#            "class_type": class_type, "aircraft": aircraft}
    

for i, f in enumerate(flights):
    print('flight', i)
    result_set = process_flight(f)
    for (k, v) in result_set.items():
        print(k, ':', v)