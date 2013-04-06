from operator import add
from functools import reduce
from collections import namedtuple


def printGroups(allData):
    headers = [
        "Match Number",
        "Group Number",
        "Match Name",
        "Match",
        ]

    # agregate the passed data and find out table dimensions
    columns = namedtuple('colums', ['matchNumbers', 'groupNumbers', 'matchNames', 'matches'])
    columnData = columns(*zip(*allData))
    columnMaxes = columns(*[maxlen(curColumn, headers[index]) for index, curColumn in enumerate(columnData)])
    totalLengths = reduce(add, columnMaxes)

    # build all row formatters as well as the divider
    divider = '+' + '-' * (totalLengths + 3) + '+'
    basicFormatter = "{{[{1}]: ^{0}}}"
    headerStrings = ['|']
    rows = [['|'] for i in range(len(allData))]

    # create a formatter for each row using the basic formatter template
    # provide an index to the formatter that corresponds to where that row is located
    # based on the return value of controllers group tuples
    columnFormatters = columns(*[basicFormatter.format(curMax, index) for index, curMax in enumerate(columnMaxes)])

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
    maxVal = max(iterable, key=lambda x: len(str(x)))
    maxVal = str(maxVal)
    return len(max(maxVal, other, key=len))

if __name__ == '__main__':
    data = [(1, 1, '', 'abc'), (1, 2, 'Friendly Match', 'defghijklmno')]
    printGroups(data)
