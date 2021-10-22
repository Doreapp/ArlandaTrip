

def exportMarkdown(filename:str, trips:list):
    '''
    Export the trips list into a Markdown file (.md)
    Will fill the markdown file with a table

    :param: filename (str) - name of the file to export in. Will override content. Includes extension (.md)
    :param: trips (list) - list of trips to exports. Not empty.
    '''
    text = ''

    # Header
    firstOption = trips[0]
    text = 'Day' + '|'
    text += firstOption[0].start.name+'|'
    text += "Line Number"+'|'
    text += firstOption[0].end.name+'|' 
    text += firstOption[1].start.name+'|'
    text += "Line Number"+'|'
    text += firstOption[1].end.name+"\n"
    text += '---|---|---|---|---|---|---\n'

    formatDay = '%d/%m/%Y'
    formatTime = "%H:%M"

    # Lines
    for trip in trips:
        first = trip[0]
        text += first.start.time.strftime(formatDay)+'|'
        text += first.start.time.strftime(formatTime)+'|'
        text += first.lineNumber+'|'
        text += first.end.time.strftime(formatTime)+'|'
        second = trip[1]
        text += second.start.time.strftime(formatTime)+'|'
        text += second.lineNumber+'|'
        text += second.end.time.strftime(formatTime)+'|'
        text += '\n'
    
    file = open(filename, 'w', encoding='utf-8')
    file.write(text)
    file.close()

def exportCSV(filename:str, trips:list, separator=';'):
    '''
    Export the trips list into a CSV file

    :param: filename (str) - name of the file to export in. Will override content. Includes extension (.csv)
    :param: trips (list) - list of trips to exports. Not empty.
    :param: separator (str) [Optional] - separator of arguments on a same line. Default: ';'
    '''
    text = ''

    # Header
    firstOption = trips[0]
    text = 'Day' + separator
    text += firstOption[0].start.name+separator
    text += "Line Number"+separator
    text += firstOption[0].end.name+separator 
    text += firstOption[1].start.name+separator
    text += "Line Number"+separator
    text += firstOption[1].end.name+"\n"

    formatDay = '%d/%m/%Y'
    formatTime = "%H:%M"

    # Lines
    for trip in trips:
        first = trip[0]
        text += first.start.time.strftime(formatDay)+separator
        text += first.start.time.strftime(formatTime)+separator
        text += first.lineNumber+separator
        text += first.end.time.strftime(formatTime)+separator
        second = trip[1]
        text += second.start.time.strftime(formatTime)+separator
        text += second.lineNumber+separator
        text += second.end.time.strftime(formatTime)+separator
        text += '\n'
    
    file = open(filename, 'w')
    file.write(text)
    file.close()
