'''
Created on May 15, 2018

@author: jahre
'''

import re
from calplotCore import fatal, NO_DATA_STRING, warn, normalize, isFloat

redPrefix   = '\033[1;31m'
greenPrefix = '\033[1;32m'
colorSuffix = '\033[1;m'

def readDataFile(datafile, columns, onlyWlType):
    header = datafile.readline().strip().split()
    data = []
    for l in datafile:
        rawline = l.strip().split()
        if rawline == []:
            continue
        tmp = [rawline[0]]
        
        error = False
        for e in rawline[1:]:
            if e == "N/A":
                error = True
                continue
            elif e == "RM":
                error = True
                continue
            elif e == NO_DATA_STRING:
                tmp.append(None)
                continue
            
            try:
                tmp.append(float(e))
            except:
                fatal("Parse error, cannot convert "+e+" to float")
        
        if not error:
            if onlyWlType != "":
                wlString = tmp[0].split("-")
                if wlString[1] != onlyWlType:
                    continue
            
            data.append(tmp)
    
    if len(header) != len(data[0])-1:
        fatal("Datafile parse error, header has length "+str(len(header))+", data length is "+str(len(data[0])))
    
    if columns != "":
        colstrs = columns.split(",")
        includelist = [float(s) for s in colstrs]
        
        newheader = []
        for i in range(len(header)):
            if i in includelist:
                newheader.append(header[i])
        
        newdata = []
        for l in data:
            newline = [l[0]]
            for i in range(len(header)):
                if i in includelist:
                    newline.append(l[i+1])
            newdata.append(newline)
        
        return newheader, newdata
    
    return header, data

def readFilesForMerge(filenames, separator, columnPrefix, quiet):
    
    data = []
    
    for fileID in range(len(filenames)):
        filename = filenames[fileID]
        curFile = open(filename)
        
        first = True
        fileRows = []
        numVals = 0
        
        for line in curFile:
            if first:
                head = re.split(separator, line.strip())
                firstLength = len(head) 
                first = False
            else:
                values = re.split(separator, line.strip())
                if numVals != 0:
                    if len(values) != numVals:
                        if not quiet:
                            warn("Cannot parse line: "+str(line.strip()))
                        continue
                numVals = len(values)
                
                fileRows.append(values)
                
        if not (firstLength == numVals or firstLength == numVals-1):
            fatal("Unknown header format in file "+filename+", possibly a parse error") 
        
        if columnPrefix != "":
            try:
                prefix = columnPrefix.split(",")[fileID]
            except:
                fatal("Column prefix parse error in string"+columnPrefix)
            
            for i in range(len(head)):
                head[i] = prefix+head[i]
        
        data.append( (head, fileRows, numVals, filename) )
    
    return data

def createDataSeries(rawdata, datacols, plotType, fixWls, onlyWlNum):
    dataseries =[[] for i in range(datacols+1)]
    
    for l in rawdata:
        for i in range(datacols+1):
            if plotType == "scatter":
                dataseries[i].append(l[i])
            elif l[i] != NO_DATA_STRING:
                dataseries[i].append(l[i])

    if fixWls:
        newWls = []
        for wlbm in dataseries[0]:
            wlbmlist = wlbm.split("-")
            wl = wlbmlist[1]+"-"+wlbmlist[2]
            
            if wlbmlist[-2] == "s6":
                bm = wlbmlist[-2]+"-"+wlbmlist[-1]
            else:
                bm = wlbmlist[-1][:-1]
            
            newWls.append(wl+"_"+bm)
            
        dataseries[0] = newWls
        
    if onlyWlNum:
        newWls = []
        for wl in dataseries[0]:
            tmp = wl.split("-")
            newWls.append(tmp[-1])
        
        dataseries[0] = newWls

    return dataseries

def colorCodeOffsets(text, doColor):
    if not doColor:
        return text
    
    if not isFloat(text):
        return text
    
    floatVal = float(text)
    
    if floatVal == 1.0:
        return text
    
    if floatVal > 1.0:
        return greenPrefix+text+colorSuffix
    
    return redPrefix+text+colorSuffix

def justify(text, left, width):
    
    if colorSuffix not in text:
        padding = width - len(text)
    else:
        tmpText = text.replace(colorSuffix, "")
        tmpText = tmpText.replace(redPrefix, "")
        tmpText = tmpText.replace(greenPrefix, "")
        padding = width - len(tmpText)
    
    padStr = ""
    for i in range(padding):
        padStr += " "
    
    if left:
        return text+padStr
    return padStr+text

def printData(textarray, leftJust, outfile, decimals, **kwargs):

    if "normalizeToColumn" in kwargs:        
        normalizeToColumn = kwargs["normalizeToColumn"]
    else:
        normalizeToColumn = -1
    
    if "colorCodeOffsets" in kwargs:
        doColor = kwargs["colorCodeOffsets"]
    else:
        doColor = False
    
    if textarray == []:
        raise ValueError("array cannot be empty")
    if textarray[0] == []:
        raise ValueError("array cannot be empty")
    if len(textarray[0]) != len(leftJust):
        raise ValueError("justification array must be the same with as the rows")
    
    if normalizeToColumn != -1:
        textarray = normalize(textarray, normalizeToColumn, decimals)
    
    padding = 2
    
    colwidths = [0 for i in range(len(textarray[0]))]
    
    for i in range(len(textarray)):
        for j in range(len(textarray[i])):
            if not (isinstance(textarray[i][j], str) or isinstance(textarray[i][j], unicode)):
                raise TypeError("all printed elements must be strings")
            
            if len(textarray[i][j]) + padding > colwidths[j]:
                colwidths[j] = len(textarray[i][j]) + padding
    
    
    for i in range(len(textarray)):
        for j in range(len(textarray[i])):
            print >> outfile, justify(colorCodeOffsets(textarray[i][j], doColor),
                                      leftJust[j],
                                      colwidths[j]),
        print >> outfile, ""
    