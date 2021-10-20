# Arlanda

Python script to search for routes from **Odenplan** station to **Arlanda** airport without paying the fee at the airport. 
The strategy itself is to take a commuter train (40/41/42X) from Odenplan to Märsta station and then a bus (843) from Märsta to Arlanda.

**Why ?** SL app doesn't propose the bus 843 and google maps doesn't propose the commuter trains. 

## SL API

In order to get correct timetables (that are evolving throught the time), the script is fetching the departure using [SL API](https://developer.trafiklab.se/)

**TODO explain more about that**

