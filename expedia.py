#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 23:01:10 2017

@author: RockyYeung
"""
import bs4 as bs
import requests
import json


"""
source: jfk
destination: mia
date: 01/01/2018
"""
def parse(source, destination, date):
    try:
        url = "https://www.orbitz.com/Flights-Search?trip=oneway&leg1=from:{},to:{},departure:{}TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www.orbitz.com".format(source, destination, date)
        print(url)
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, 'lxml')
        # check the page is not disambiguise
        
        try:
            json_data_xpath = soup.find('script', {'id': 'cachedResultsJson'}).text
        except AttributeError:
            print('Airport too small, skip')
            return []
        raw_json = json.loads(json_data_xpath)
        flight_data = json.loads(raw_json['content'])

        
        lists = []
        
        
        for k, v in flight_data['legs'].items():
            no_of_stops = v["stops"]
            if no_of_stops==0:
                stop = "Nonstop"
            else:
                continue
            
            total_distance =  v["formattedDistance"]
            exact_price = v['price']['totalPriceAsDecimal']
            departure_location_city = v['departureLocation']['airportCity']
            departure_location_airport_code = v['departureLocation']['airportCode']
            
            arrival_location_airport_code = v['arrivalLocation']['airportCode']
            arrival_location_city = v['arrivalLocation']['airportCity']
            airline_name = v['carrierSummary']['airlineName']
            
            flight_duration = v['duration']
            flight_hour = flight_duration['hours']
            flight_minutes = flight_duration['minutes']
            flight_days = flight_duration['numOfDays']
    

    
            total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days,flight_hour,flight_minutes)
            departure = departure_location_airport_code+", "+departure_location_city
            arrival = arrival_location_airport_code+", "+arrival_location_city
            carrier = v['timeline'][0]['carrier']
            plane = carrier['plane']
            plane_code = carrier['planeCode']
            formatted_price = "{0:.2f}".format(exact_price)
    
            if not airline_name:
                airline_name = carrier['operatedBy']
            
            timings = []
            for timeline in v['timeline']:
                if 'departureAirport' in timeline.keys():
                    departure_airport = timeline['departureAirport']['longName']
                    departure_time = timeline['departureTime']['time']
                    arrival_airport = timeline['arrivalAirport']['longName']
                    arrival_time = timeline['arrivalTime']['time']
                    flight_timing = {
                                        'departure_airport':departure_airport,
                                        'departure_time':departure_time,
                                        'arrival_airport':arrival_airport,
                                        'arrival_time':arrival_time
                    }
                    timings.append(flight_timing)
    
            flight_info={'stops':stop,
                'total distance': total_distance,
                'ticket price':formatted_price,
                'departure':departure,
                'arrival':arrival,
                'flight duration':total_flight_duration,
                'airline':airline_name,
                'plane':plane,
                'departure_airport':departure_airport,
                'departure_time':departure_time,
                'arrival_airport':arrival_airport,
                'arrival_time':arrival_time,
                'plane code':plane_code
            }
            lists.append(flight_info)
        sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
        return sortedlist
    except ValueError:
        print ('Value error')
    
    return {"error":"failed to process the page",}

#if __name__=="__main__":
#	argparser = argparse.ArgumentParser()
#	argparser.add_argument('source',help = 'Source airport code')
#	argparser.add_argument('destination',help = 'Destination airport code')
#	argparser.add_argument('date',help = 'MM/DD/YYYY')
#
#	args = argparser.parse_args()
#	source = args.source
#	destination = args.destination
#	date = args.date
#	print("Fetching flight details")
#	scraped_data = parse(source,destination,date)
#	print("Writing data to output file")
#	with open('/Users/RockyYANG/Desktop/game/data/{}-{}-flight-results.json'.format(source,destination),'w') as fp:
#	 	json.dump(scraped_data,fp,indent = 4)