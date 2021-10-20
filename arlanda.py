
# TODO exports the results
# TODO handle command line args

import requests
import datetime
from arlanda_gui import GUI
from arlanda_parser import Trip, parse

# https://developer.trafiklab.se/api/resrobot-reseplanerare/konsol

# 2 possibilities
#   * Use the console-GUI process, that ask for information along the way
#   * Use the command line based implementation
#
# Decision tree
# 
# Go from or to arlanda: From(F) - Go(G)
# (F)/(G) -> select departure or arrival time: Departure(D) - Arrival(A) 
# (D) -> Now(N) or Later(L)
# (A/DL) -> Input the day dd/mm and then the time with format hh:mm
# -> Search for it
# 
# Args TODO

# IDS map, from stop name to its id
ids = dict()
ids["Märsta"] = 740000027
ids["Odenplan"] = 740001618
ids["Arlanda"] = 740020671

# API Key
API_KEY = ''

def api_call(key:str, originId:int, destId:int, date:str, time:str, searchForArrival:bool, filename:str='.cache')->str:
    '''
    Call the API

    :param: key (str) - API Key 
    :param: originId (int) - Id of the origin station
    :param: destId (int) - Id of the destination station
    :param: date (str) - date string for the research, with format yyyy-mm-dd
    :param: time (str) - time string for the research, with format hh:mm
    :param: searchForArrival (bool) - are we searching for an arrival time ?
    :param: filename (str) [Optional] - file name for saving the result
    :return: json (str) - result for the call, in json format
    :see: https://developer.trafiklab.se/node/25593/
    '''

    # Build the url
    url ='https://api.resrobot.se/v2/trip?key='+key
    url = url + '&originId='+str(originId)
    url = url + '&destId='+str(destId)
    url = url + '&passlist=0'
    url += '&date='+date
    url += '&time=' + time
    if searchForArrival:
        url += '&searchForArrival=1'  
    url += '&format=json'
    
    print("Calling API...")
    response = requests.get(url)
    
    cacheFile = open(filename+'.json','wb')
    cacheFile.write(response.content)
    cacheFile.close()
    
    return response.content.decode()

def merge_trips(firsts:Trip, seconds:Trip, correspondanceMin:int=5)->list:
    '''
    Merge 2 trip list in one. 
    The resulting trips starts with a trip from the `firsts` list, continue
    with a wait time of at least `correspondanceMin` minutes, and end with a 
    trip of the `seconds` list

    :param: first (list) - List of the trips available for the first route
    :param: second (list) - List of the trips available for the second route
    :param: correspondanceMin (int) [Optional] - time of the minimum corresponance, in minutes. Default is 5
    :return: trips (list) - list of the results trips (array of 2 trips)
    '''
    print("Merge trips...")
    results = []

    # Min correspondance time
    minDelta = datetime.timedelta(seconds=5*60)
    
    firstIndex = 0
    secondIndex = 0
    while firstIndex < len(firsts) and secondIndex < len(seconds):
        if seconds[secondIndex].start.time - firsts[firstIndex].end.time >= minDelta:
            # It matches
            results.append((firsts[firstIndex], seconds[secondIndex]))
            firstIndex += 1
        else:
            secondIndex += 1
    return results

def request(isFrom:bool, isDeparture:bool, date:str, time:str) -> list:
    '''
    Request the path with corresponding params

    :param: isFrom (bool) - Is the route from Arlanda. False means from Odenplan
    :param: isDeparture (bool) - Is the requested time the departure time. False means it's the arrival time
    :param: date (str) - departure/arrival date. Format yyyy-mm-dd
    :param: time (str) - departure/arrival time. Format hh:mm
    :return: trips (list) - list of available trips
    '''
    if isFrom:
        print("Request from arlanda")
        jsonAtoM = api_call(API_KEY, ids['Arlanda'], ids['Märsta'], date, time, not isDeparture, 'atm')
        jsonMtoO = api_call(API_KEY, ids['Märsta'], ids['Odenplan'], date, time, not isDeparture, 'mto')
        firsts = parse(jsonAtoM)
        seconds = parse(jsonMtoO)
    else: 
        print("Request to arlanda")
        jsonOtoM = api_call(API_KEY, ids['Odenplan'], ids['Märsta'], date, time, not isDeparture, 'otm')
        jsonMtoA = api_call(API_KEY, ids['Märsta'], ids['Arlanda'], date, time, not isDeparture, 'mta')
        firsts = parse(jsonOtoM)
        seconds = parse(jsonMtoA)
    
    trips = merge_trips(firsts, seconds)
    return trips


def print_results(results:list):
    '''
    Print the results trips properly

    :param: results (list) - list of trips to print
    '''
    formatTime = "%a %d %H:%M"
    print("Results:")
    for trip in results:
        first = trip[0]
        print("-------------------------------")
        print("    "+first.start.time.strftime(formatTime)+" - "+first.start.name)
        print("        Take ["+first.lineNumber+"] towards '"+first.lineDirection+"'")
        print("    "+first.end.time.strftime(formatTime)+" - "+first.end.name)
        print("        ...")
        second = trip[1]
        print("    "+second.start.time.strftime(formatTime)+" - "+second.start.name)
        print("        Take ["+second.lineNumber+"] towards '"+second.lineDirection+"'")
        print("    "+second.end.time.strftime(formatTime)+" - "+second.end.name)


if __name__ == '__main__':
    try:
        apiKeyFile = open('api_key.key', 'r')
        API_KEY = apiKeyFile.read()
    except:
        print("Error while reading the API Key. Make sure your API key is stored in 'api_key.key'")
        exit(1)

    isFrom, isDeparture, date, time = GUI().getInfo()
    print("is from: ", isFrom)
    print("is departure: ", isDeparture)
    print("date", date)
    print("time", time)

    trips = request(isFrom, isDeparture, date, time)
    print_results(trips)
