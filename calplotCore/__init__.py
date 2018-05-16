'''
Created on May 15, 2018

@author: jahre
'''

import sys

NO_DATA_STRING = "NoData"

def fatal(message):
    print
    print "ERROR: "+message
    print
    sys.exit(-1)
    
def numberToString(number, decimalPlaces):
    if type(number) == type(int()):
        return str(number)
    elif type(number) == type(float()):
        return ("%."+str(decimalPlaces)+"f") % number
    elif type(number) == type(dict()):
        return "Dictionary"
    assert type(number) == type(str())
    return number