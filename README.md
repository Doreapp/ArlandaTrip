# Arlanda

Python script to search for routes from **Odenplan** station to **Arlanda** airport without paying the fee at the airport. 
The strategy itself is to take a commuter train (40/41/42X) from Odenplan to Märsta station and then a bus (843) from Märsta to Arlanda.

**Why ?** SL app doesn't propose the bus 843 and google maps doesn't propose the commuter trains. 

## SL API

In order to get correct timetables (that are evolving throught the time), the script is fetching the departure using [SL API](https://developer.trafiklab.se/)

We are using [SL Travel Planner](https://developer.trafiklab.se/api/sl-reseplanerare-31) to get the trips from 
1. Odenplan to Märsta,
2. Märsta to Arlanda.

Then, we are merging the result to show available trips

## Setup

1. Git clone
    ```
    git clone https://github.com/Doreapp/ArlandaTrip.git
    cd ArlandaTrip
    ```

2. Get yourself an API Key from [SL API](https://developer.trafiklab.se/).
    
    You need to create an account, then a project, and then tell that your project requires [SL Travel Planner](https://developer.trafiklab.se/api/sl-reseplanerare-31). 
    After that, you'll have a free API Key, with a limited usage, that should match your needs

3. Put your api key into a file named `api_key.key` under `ArlandaTrip` folder
    

## How to use

### "GUI"

Run 
```
python3 arlanda.py
```

**Options**
* use `-h` or `--help` to display an help message, explaining each handled argument
* use `-kf` or `--key-file` to set the actual location of the file where is stored your API key (by default, it will use `api_key.key` file)
* use `-xf` or `--export-file` to request the export of the result in an external file. Specify the file you want the export to be in.
    * If the extension of the file is `.md`, then a markdown file will be exported, containing a table in it
    * Otherwise, regardless of the extension, a `csv` file will be exported, with `;` as separators.


Then, answer the questions about your query

**Example**:
```
Hi, welcome to ToArlanda Schedule searcher
Are you going from or to arlanda ?
   From(F) - To(T)
T
Do you want to search for a departure or arrival time ?
   Departure(D) - Arrival(A)
A
   Today? Yes(Y) - No(N)
Y
   At what time ? - Format hh:mm
19:00
Calling API...
Calling API...
Merging trips...
Results:
-------------------------------
    Wed 20 17:02 - Stockholm Odenplan station
        Take [41] towards 'Märsta station (Sigtuna kn)'
    Wed 20 17:37 - Märsta station (Sigtuna kn)
        ...
    Wed 20 17:47 - Märsta station (Sigtuna kn)
        Take [583] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:00 - Arlanda terminal 2-3 buss (Sigtuna kn)
-------------------------------
    Wed 20 17:17 - Stockholm Odenplan station
        Take [41] towards 'Märsta station (Sigtuna kn)'
    Wed 20 17:52 - Märsta station (Sigtuna kn)
        ...
    Wed 20 18:02 - Märsta station (Sigtuna kn)
        Take [583] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:15 - Arlanda terminal 2-3 buss (Sigtuna kn)
-------------------------------
    Wed 20 17:32 - Stockholm Odenplan station
        Take [41] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:07 - Märsta station (Sigtuna kn)
        ...
    Wed 20 18:17 - Märsta station (Sigtuna kn)
        Take [583] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:30 - Arlanda terminal 2-3 buss (Sigtuna kn)
-------------------------------
    Wed 20 17:47 - Stockholm Odenplan station
        Take [41] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:22 - Märsta station (Sigtuna kn)
        ...
    Wed 20 18:32 - Märsta station (Sigtuna kn)
        Take [583] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:45 - Arlanda terminal 2-3 buss (Sigtuna kn)
-------------------------------
    Wed 20 18:02 - Stockholm Odenplan station
        Take [41] towards 'Märsta station (Sigtuna kn)'
    Wed 20 18:37 - Märsta station (Sigtuna kn)
        ...
    Wed 20 18:47 - Märsta station (Sigtuna kn)
        Take [583] towards 'Märsta station (Sigtuna kn)'
    Wed 20 19:00 - Arlanda terminal 2-3 buss (Sigtuna kn)
```
