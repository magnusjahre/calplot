'''
Created on May 15, 2018

@author: jahre
'''

import sys

NO_DATA_STRING = "NoData"
ERROR_STRING = "N/A"
TYPED_WORKLOAD_IDENTIFIERS = ["h", "m", "l", "s", "a"]


def fatal(message):
    print(f"\nERROR: {message}\n")
    sys.exit(-1)


def warn(message):
    print(f"WARNING: f{message}")


def numberToString(number, decimalPlaces):
    if isinstance(number, int):
        return str(number)
    elif isinstance(number, float):
        return f"{number:.{decimalPlaces}f}"
    elif isinstance(number, dict):
        return "Dictionary"
    assert isinstance(number, str)
    return number


def isInt(valStr):
    try:
        int(valStr)
        return True
    except ValueError:
        return False


def isFloat(valStr):
    try:
        float(valStr)
        return True
    except ValueError:
        return False


def normalize(data, toColumnID, decimals):
    newdata = []
    newdata.append(data[0])
    for i in range(len(data))[1:]:
        for j in range(len(data[i])):
            if j == 0:
                newdata.append([data[i][j]])
            else:
                if toColumnID >= len(data[i]):
                    raise Exception("Column ID does not exist, must be in the range from 1 to "+str(len(data[i])-1))

                if data[i][j] == ERROR_STRING or data[i][toColumnID] == ERROR_STRING:
                    normval = 0.0
                else:
                    try:
                        normval = (float(data[i][j]) / float(data[i][toColumnID]))-1.0
                    except Exception:
                        raise Exception(f"Normalization failed on elements {data[i][j]} and {data[i][toColumnID]}")
                newdata[i].append(numberToString(normval, decimals))

    return newdata
