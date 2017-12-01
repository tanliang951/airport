#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 12:28:22 2017

@author: RockyYeung
"""

from selenium import webdriver
import bs4 as bs
from selenium.common.exceptions import WebDriverException

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)

"""
    from_ = "LAX"
    to = "DCA"
    date = "12/01/2017"
"""
def main():
    
    dept = "BOS"
    arrv = "LAX"
    date = "12/01/2017"
    """
    dept = input("From: ")
    arrv = input("To: ")
    date = input("Date (MM/DD/YYYY): ")
    """
    print("Flying from {} to {} on {}".format(dept, arrv, date))
    print("Receiving web page...")
    fly(dept, arrv, date)
    

def fly(dept, arrv, date):
    url_temp = "https://www.orbitz.com/Flights-Search?trip=oneway&leg1=from:{from_},to:{to},\
    departure:{date}TANYT&passengers=children:0,adults:1,seniors:0,\
    infantinlap:Y&options=maxhops%3A0&mode=search"
    url = url_temp.format(from_=dept, to=arrv, date=date)
    #print("Vising:\n", url)
    driver.get(url)
    driver.implicitly_wait(10)
    # check at least one flight exists

    if bs.BeautifulSoup(driver.page_source, 'lxml').find('ul', {'id': "flightModuleList"}) == None:
        print("No flights found at this day, return []")
        return []
    
    expand_buttons = driver.find_elements_by_class_name("show-flight-details")
    
    def process_flight(f):
        try:
            dept_time = f.find("span", {"class": "departure-time departure-0-emphasis",
                                "data-test-id": "departure-time"}).text.strip()
        except:
            raise Exception("dept_time is not found")
        try:
            arrv_time = f.find("span", {"class": "arrival-time arrival-0-emphasis",
                                    "data-test-id": "arrival-time"}).text.strip()
        except:
            raise Exception("arrv_time is not found")
        
        try:
            duration = f.find("div", {"class": "primary duration-emphasis",
                                      "data-test-id": "duration"}).text.strip()
        except:
            raise Exception("duration is not found")
            
        try:
            # LAX - DCA
            airport_from, airport_to = f.find("div", {"class": "secondary", "data-test-id": "airports"}).text.strip().split(" - ")
        except:
            raise Exception("airports are not found")
        
        try:
            airline_name = f.find("div", {"class": "secondary truncate", 
                                      "data-test-id": "airline-name"}).text.strip()
        except:
            raise Exception("airline name is not found")
        try:
            # American Airlines 52, dynamically loaded
            flight_number = f.find("dd", {"class": "flight", 
                                      "data-test-id": "details-airline-data"}).text.strip()
        except:
            raise Exception("flight number is not found")
        # 2,295 mi
        distance = f.find("dd", {"class": "details-utility-item-value"}).text.strip()
        class_type = f.find("dd", {"data-test-id": "details-class-type"}).text.strip()
        items = f.find("dd", {"class": "aircraft"}).text.strip().split('|')
        aircraft = items[0].strip()
            
        return {"dept_time": dept_time, "arrv_time": arrv_time, 
                "duration": duration, "airline-name": airline_name,
                "airport_from": airport_from, "airport_to": airport_to,
                "flight_number": flight_number, "distance": distance,
                "class_type": class_type, "aircraft": aircraft}
    
    
    
    # click all expand buttons
    print("Expand to get more information...")
    for idx, button in enumerate(expand_buttons):
#        print('click to expand flight', idx)
        try:
            button.click()
        except WebDriverException:
            driver.get_screenshot_as_file('~/Desktop/screen.png')
            print("fail to click button, screenshot saved")
            raise
            
#    print("Expand Done.\n")
    
    
    # load the html source at this time into soup
    soup = bs.BeautifulSoup(driver.page_source, 'lxml')
    flights = soup.find('ul', {'id': "flightModuleList"}).find_all('li', {'class': ["flight-module", "segment", "offer-listing"]})
    if len(flights) == 0:
        print("No flights found at this day, return []")
    data = []
    for i, thisFlight in enumerate(flights):
        #print('---Flight', str(i)+'---')
        try:
            datai = process_flight(thisFlight)
        except:
         #   print("Fields are missing, dispose this flight")
        #    print("")
            continue
        #for key, value in datai.items():
         #   print(key, ':', value)
        #print("")
        data.append(datai)
    print("Found {} flights".format(len(data)))
    return data

    
if __name__ == '__main__':
    main()