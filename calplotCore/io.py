'''
Created on May 15, 2018

@author: jahre
'''

from calplotCore import fatal, NO_DATA_STRING

def readDataFile(datafile, columns, onlyWlType):
    header = datafile.readline().strip().split()
    data = []
    for l in datafile:
        rawline = l.strip().split()
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
                tmp.append(NO_DATA_STRING)
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

def getScatterData(dataseries):
    xdata = [[] for i in range(len(dataseries)-1)]
    ydata = [[] for i in range(len(dataseries)-1)]
    
    for i in range(len(dataseries[1:])):
        for j in range(len(dataseries[0])):
            if dataseries[i+1][j] != NO_DATA_STRING:
                xdata[i].append(dataseries[0][j])
                ydata[i].append(dataseries[i+1][j])
                
    return xdata, ydata