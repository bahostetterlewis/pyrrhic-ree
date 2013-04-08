from operator import add, or_, xor
from functools import reduce
from collections import namedtuple
import re


import controller
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


FLAG_TO_LETTER = {
    re.ASCII: 'a',
    re.IGNORECASE: 'i',
    re.LOCALE: 'L',
    re.MULTILINE: 'm',
    re.DOTALL: 's',
    re.VERBOSE: 'x',
    }

LETTER_TO_FLAG = {
    'a': re.ASCII,
    'i': re.IGNORECASE,
    'l': re.LOCALE,
    'm': re.MULTILINE,
    's': re.DOTALL,
    'x': re.VERBOSE,
    }


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

    def maxlen(iterable, other):
        '''
        Utility used to determine row widths when creating tables
        Gets the max length string in the iterable and returns the max betweent that and other
        '''
        maxVal = max(iterable, key=lambda x: len(str(x)))
        maxVal = str(maxVal)
        return len(max(maxVal, other, key=len))

    # agregate the passed data and find out table dimensions
    columns = namedtuple('colums', ['matchNumbers', 'groupNumbers', 'matchNames', 'matches'])
    columnData = columns(*zip(*allData))
    columnMaxes = columns(*(maxlen(curColumn, curHeader) for curColumn, curHeader in zip(columnData, headers)))
    totalLengths = reduce(add, columnMaxes)

    # build all row formatters as well as the divider
    divider = '+' + '-' * (totalLengths + 3) + '+'
    basicFormatter = "{{[{1}]: ^{0}}}"
    headerStrings = []
    rows = [[] for i in enumerate(allData)]

    # create a formatter for each row using the basic formatter template
    # index represents the current column the formatter will belong to
    # This allows us to index the row tuple in the formatter itself using the [] format
    columnFormatters = columns(*(basicFormatter.format(curMax, index) for index, curMax in enumerate(columnMaxes)))

    # finally print the table
    print(divider)

    # build the headers based on the padding each row needs
    for header, padding in zip(headers, columnMaxes):
        headerStrings.append('{0: ^{1}}'.format(header, padding))

    print("|{}|".format('|'.join(headerStrings)))
    print(divider)

    # use each row of data and the rows list to create each resulting row
    # then add them to the rows list for later printing
    for data, row in zip(allData, rows):
        for formatter in columnFormatters:
            row.append(formatter.format(data))

    # join each row and print it
    for row in rows:
        print("|{}|".format('|'.join(row)))

    print(divider)


def UpdatePrompt():
    mainMenu = "[P]attern [R]eplace [M]atch [F]lags [V]iew Results [Q]uit"
    print('\n' * 5)
    print("Regex:", controller.regex)
    print("Replace String:", controller.replaceString)
    print("Match String:", controller.matchString)
    print("Flags:", flagsToString())
    print(mainMenu)


def changeMatchString():
    controller.matchString = input("New match string:")


def changeRegex():
    controller.regex = input("New regex:")


def changeReplaceString():
    controller.replaceString = input("New replacement:")


def changeFlags():
    choice = input("[T]oggle flag [S]et all flags:").lower()

    if choice.startswith('t'):
        choice = input("Flag[aiLmxs]:").lower()
        modifyFlags(xor, choice)
    else:
        choice = input("New flags[aiLmxs]:").lower()
        controller.flags = 0
        modifyFlags(or_, choice)


def modifyFlags(operation, flagString):
    controller.togglePause()
    for flag in flagString:
        if flag in 'ailmxs':
            controller.flags = operation(controller.flags, LETTER_TO_FLAG[flag])
    controller.togglePause()


def viewResults():
    print('view results')


def flagsToString():
    result = ''
    for flag in FLAG_TO_LETTER:
        if flag & controller.flags:
            result += FLAG_TO_LETTER[flag]
    return result


def Run():
    controller.updateView = UpdatePrompt
    UpdatePrompt()
    choice = input().lower()
    while not choice.startswith('q'):
        if choice.startswith('p'):
            changeRegex()
        elif choice.startswith('m'):
            changeMatchString()
        elif choice.startswith('r'):
            changeReplaceString()
        elif choice.startswith('f'):
            changeFlags()
        elif choice.startswith('v'):
            viewResults()
        elif not choice.startswith('q'):
            print('Error: <{}> is not a valid input'.format(choice))

        choice = input().lower()

if __name__ == '__main__':
    Run()
    # data = [(1, 1, '', 'abc'), (1, 2, 'Friendly Match', 'defghijklmno')]
    # printGroups(data)
