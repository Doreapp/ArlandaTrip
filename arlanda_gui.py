import datetime

def _input(possibilities, question):
    print("   "+question)
    userInput = input().strip().lower()
    if userInput in possibilities:
        return userInput
    else:
        print("Unexpected input '"+userInput+"'")
        return _input(possibilities, question)

def _input_day(question):
    print("   "+question+" - Format dd/mm/yyyy")
    userInput = input().strip()
    
    data = userInput.split("/")
    if len(data) < 3:
        print("Unexpected input '"+userInput+"', respect format dd/mm/yyyy")
        return _input_day(question)
    try:
        day = int(data[0])
        month = int(data[1])
        year = int(data[2])
    except:
        print("Unexpected input '"+userInput+"', respect format dd/mm/yyyy")
        return _input_day(question)
    
    try:
        date = datetime.datetime(year, month, day)
    except ValueError:
        print("Unexpected input, your date doesn't exists")
        return _input_day(question)

    return date

def _input_time(question):
    print("   "+question+" - Format hh:mm")
    userInput = input().strip()
    
    data = userInput.split(":")
    if len(data) < 2:
        print("Unexpected input '"+userInput+"', respect format hh:mm")
        return _input_time(question)
    try:
        hour = int(data[0])
        min = int(data[1])
    except:
        print("Unexpected input '"+userInput+"', respect format hh:mm")
        return _input_time(question)
    
    if hour < 0 or hour >= 24:
        print("Unexpected input '"+userInput+"', hours must be in [0; 24[")
        return _input_time(question)
    
    if min < 0 or min >= 60:
        print("Unexpected input '"+userInput+"', minutes must be in [0; 24[")
        return _input_time(question)

    return hour * 60 + min


def api_date(date):
    return str(date.year)+"-"+str(date.month)+"-"+str(date.day)

def api_time(minutes):
    def _(i):
        if i < 10:
            return '0'+str(i)
        return str(i)

    return _(int(minutes/60))+':'+ _(minutes%60)


class GUI:
    def getInfo(self):
        print("Hi, welcome to ToArlanda Schedule searcher")
        
        print("Are you coming or going to arlanda ?")
        fromGo = _input(['from','f','go','g'],"From(F) - Go(G)")

        print("Do you want to search for a departure or arrival time ?")
        departureArrival = _input(['departure','d','arrival','a'], "Departure(D) - Arrival(A)")

        done = False
        if departureArrival[0] == 'd':
            nowLater = _input(['now','n','later','l'], 'Now(N) - Later(L)')
            if nowLater[0] == 'n':
                dateNow = datetime.datetime.now()
                date = dateNow
                time = dateNow.hour*60 + dateNow.minute
                done = True
        if not done:
            today = _input(['yes','y','no','n'], 'Today? Yes(Y) - No(N)')
            if today[0] == 'y':
                date = datetime.datetime.now()
            else:
                date = _input_day('At what day ?')
            time = _input_time('At what time ?')

        return fromGo[0] == 'f', departureArrival[0] =='d',api_date(date), api_time(time)