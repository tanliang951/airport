#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 22:34:41 2017

@author: RockyYeung
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import bs4 as bs

"""
https://www.google.com/flights/?f=0&gl=hk#search;f=SFO;t=LAX;d=2017-12-21;r=2017-12-25;tt=o;s=0
"""

f = 'SFO'
t = 'LAX'
d = '2017-12-21'
url_temp = 'https://www.google.com/flights/?f=0&gl=hk#search;f={f};t={t};d={d};tt=o;s=0'
           

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(10)
driver.get('https://www.google.com/flights/')
print('log in...')
log_in_button = driver.find_element_by_id('gb_70')
log_in_button.click()
account = driver.find_element_by_id('identifierId')
account.send_keys('yangrq@connect.hku.hk')
next_button = driver.find_element_by_id('identifierNext')
next_button.click()
user_name = driver.find_element_by_name('j_username')
password = driver.find_element_by_name('j_password')
user_name.send_keys('yangrq')
password.send_keys('audureyhB03')
LOGIN = driver.find_element_by_xpath('//li[@class="btnLogin"]/a')
LOGIN.click()
print('successfully log in')

print('Search from {} to {} on {}'.format(f, t, d))
driver.get(url_temp.format(f=f, t=t, d=d))

soup = bs.BeautifulSoup(driver.page_source, 'lxml')
wait = WebDriverWait(driver, 10)
# 25 divs
elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, 
        '//table//table//div[@class="gwt-HTML LJV2HGB-d-P"]/div')))
flightList = elements[3:]
# filter
todo = []
for (i, flight) in enumerate(flightList):
    print('At position', i, 'in flight div list')
    # save price first
    price_with_dollar = flight.find_element_by_xpath('//div[@class="LJV2HGB-d-Ab"]').text
    # save link
    try:
        linkToFlight = flight.find_element_by_tag_name('a').get_attribute('href')
    except NoSuchElementException:
        print('Expand...')
        # click to expand
#        flight.click()
#    todo.append({
#            'link': linkToFlight,
#            'price': price_with_dollar
#                })

# then find all elements

meta_list = []
for link, price in todo:
    driver.get(link)
    info = driver.find_element_by_xpath('//div[@class="LJV2HGB-d-eb"]')
    date = info.find_element_by_xpath('//div[@class="LJV2HGB-d-jb]"').text
    time = info.find_element_by_xpath('//div[@class="LJV2HGB-d-Zb"]').text
    duration = info.find_element_by_xpath('//div[@class="LJV2HGB-d-E"]').text
    flightnoAndCompany, seatClass, jetType  = list(map(lambda s: s.strip(), 
          info.find_element_by_xpath('//div\[@class="LJV2HGB-d-N"]').text.split('·')))
    print('Fight: {} information collected'.format(flightnoAndCompany))
    meta_list.append({
        "price": price,
        "date": date,
        "time": time,
        "duration": duration,
        "flightNoAndCompany": flightnoAndCompany,
        "seatClass": seatClass,
        "jetType": jetType
        })
