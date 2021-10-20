# Module Arlanda Parser
# 
# Allows to parse results from the SL API.
# /!\ Consider that the results trips consider of only one transport type.
# 

import json
import datetime

def parseTime(date:str, hours:str) -> datetime:
    '''
    Parse a time datetime
    :param: string (str) - time string in a format hh:mm
    :return: time (datetime) - the date time
    '''
    dayData = date.split('-')
    hourData = hours.split(":")
    return datetime.datetime(int(dayData[0]), int(dayData[1]), int(dayData[2]),
        int(hourData[0]), int(hourData[1]))

class Station:
    '''
    Class describing a Station (bus/metro/train...)
    :attr: name (str) - name of the station (in swedish)
    :attr: id (int) - id of the station used for trip planning 
    :attr: lon (float) - longitude of the station
    :attr: lat (float) - latitude of the station
    '''

    def __init__(self, name:str, id:int, lon:float, lat:float):
        self.name = name
        self.id = id
        self.lon = lon
        self.lat = lat

    def __str__(self) -> str:
        return self.name

class TimestampedStation(Station):
    '''
    Timestamped station: a station reached a a certain time, a "stop"
    :see: Station
    :attr: date (datetime) - datetime of the day 
    :attr: time (int) - minutes (60*hours + minutes) of the timestamp
    '''
    def __init__(self, name:str, id:int, lon:float, lat:float, date:str, time:str):
        super().__init__(name, id, lon, lat)
        self.time = parseTime(date, time)

    def __str__(self) -> str:
        return self.name + " at "+str(self.time)

class Trip():
    '''
    Single trip, between tow timestamped stations

    :attr: start (TimestampedStation) - start point of the trip
    :attr: end (TimestampedStation) - end point of the trip
    :attr: lineNumber (str) - name (mostly number) of the line used
    :attr: lineDirection (str) - name of the end station of the line used
    :see: TimestampedStation 
    '''
    def __init__(self, start:TimestampedStation, end:TimestampedStation, lineNumber:str, lineDirection:str):
        self.start = start
        self.end = end
        self.lineNumber = lineNumber
        self.lineDirection = lineDirection

    def __str__(self) -> str:
        return '['+self.lineNumber+'] '+str(self.start)+" --> "+str(self.end)


def parseTimestampedStation(raw) -> TimestampedStation:
    '''
    Parse a timestamped station saved into a json
    :param: raw (JsonObject) - json object to parse
    :return: timestampedStation (TimestampedStation) - parsed TimestampedStation
    '''
    return TimestampedStation(
        raw['name'],
        int(raw['id']),
        raw['lon'],
        raw['lat'],
        raw['date'],
        raw['time']
    )

def parseTrip(trip) -> Trip:
    '''
    Parse a trip object from a raw json
    :param: trip (JsonObject) - Input from the json to parse
    :return: trip (Trip) - parsed Trip
    '''
    tmp = trip['LegList']['Leg'][0] # The actual trip (only 1st transport is considered)

    start = parseTimestampedStation(tmp['Origin'])
    end = parseTimestampedStation(tmp['Destination'])
    lineNumber = tmp['transportNumber']
    lineDirection = tmp['direction']

    return Trip(start, end, lineNumber, lineDirection)

def parseTripArray(array) -> list:
    '''
    Parse a trip array from a raw json object
    :param: array (JsonArray) - Array to parse
    :return: trips (list) - list of trips 
    '''
    possibilities = []
    for trip in array:
        possibilities.append(parseTrip(trip))
    return possibilities

def parseRoot(root) -> list:
    '''
    Parse the root of the json
    :param: root (JsonObject) - object to parse, root of the file
    :return: trips (list) - list of parsed trips
    '''
    return parseTripArray(root["Trip"])

def parse(string:str) -> list:
    '''
    Parse a json string and read the trips in it
    :param: string (str) - json string 
    :return: trips (list) - parsed list of trip 
    '''
    root = json.loads(string)
    return parseRoot(root)

if __name__ == '__main__':
    print("Test arlanda_parser")
    cacheFile = open('.cache.json','r')
    result = parse(cacheFile.read())
    print(str([str(x) for x in result]))