from operator import add
from functools import reduce
from collections import namedtuple
import re


from ReeController import controller
controller = controller.Controller

'''
CLI Globals
'''
# FLAG_CALLS = {
#     'a': lambda: updateFlags(re.ASCII),
#     'i': lambda: updateFlags(re.IGNORECASE),
#     'L': lambda: updateFlags(re.LOCALE),
#     'm': lambda: updateFlags(re.MULTILINE),
#     's': lambda: updateFlags(re.DOTALL),
# }


# def updateFlags(flag):
#     controller.flags ^= flag


def printGroups(allData):
    '''
    Takes a list of 4-tuples and displays them in an ascii table.

    The columns are dynamically sized to fit the largest data to be displayed in
    that column. Used to pretty print groups returned from the controller.
    '''
    if not allData:
        print('No groups')
        return

    headers = [
        "Match Number",
        "Group Number",
        "Match Name",
        "Match",
        ]

    # agregate the passed data and find out table dimensions
    columns = namedtuple('colums', ['matchNumbers', 'groupNumbers', 'matchNames', 'matches'])
    columnData = columns(*zip(*allData))
    columnMaxes = columns(*(maxlen(curColumn, curHeader) for curColumn, curHeader in zip(columnData, headers)))
    totalLengths = reduce(add, columnMaxes)

    # build all row formatters as well as the divider
    divider = '+' + '-' * (totalLengths + 3) + '+'
    basicFormatter = "{{[{1}]: ^{0}}}"
    headerStrings = ['|']
    rows = [['|'] for i in enumerate(allData)]

    # create a formatter for each row using the basic formatter template
    # index represents the current column the formatter will belong to
    # This allows us to index the row tuple in the formatter itself using the [] format
    columnFormatters = columns(*(basicFormatter.format(curMax, index) for index, curMax in enumerate(columnMaxes)))

    # finally print the table
    print(divider)

    # build the headers based on the padding each row needs
    for header, padding in zip(headers, columnMaxes):
        headerStrings.append('{0: ^{1}}'.format(header, padding))
        headerStrings.append('|')

    print(''.join(headerStrings))
    print(divider)

    # use each row of data and the rows list to create each resulting row
    # then add them to the rows list for later printing
    for data, row in zip(allData, rows):
        for formatter in columnFormatters:
            row.append(formatter.format(data))
            row.append('|')

    # join each row and print it
    for row in rows:
        print(''.join(row))

    print(divider)


def maxlen(iterable, other):
    '''
    Utility used to determine row widths when creating tables
    Gets the max length string in the iterable and returns the max betweent that and other
    '''
    maxVal = max(iterable, key=lambda x: len(str(x)))
    maxVal = str(maxVal)
    return len(max(maxVal, other, key=len))


def UpdateDisplay():
    print('updating display')


def changeRegex():
    print('changing regex')


def changeSearchString():
    print('changing search string')


def changeReplaceString():
    print('changing replace')


def changeFlags():
    print('changing flags')


def changeResultsDisplay():
    print('changing results display')


def Run():
    controller.UpdateDisplay = UpdateDisplay  # set the callback
    mainMenu = "[P]attern [S]earch [R]eplace [F]lags [V]iew Results [Q]uit"
    print(mainMenu)
    choice = input().lower()
    while not choice.startswith('q'):
        if choice.startswith('p'):
            changeRegex()
        elif choice.startswith('s'):
            changeSearchString()
        elif choice.startswith('r'):
            changeReplaceString()
        elif choice.startswith('f'):
            changeFlags()
        elif choice.startswith('v'):
            changeResultsDisplay()
        elif not choice.startswith('q'):
            print('Error: <{}> is not a valid input'.format(choice))

        print(mainMenu)
        choice = input().lower()

if __name__ == '__main__':
    Run()
    # data = [(1, 1, '', 'abc'), (1, 2, 'Friendly Match', 'defghijklmno')]
    # printGroups(data)
