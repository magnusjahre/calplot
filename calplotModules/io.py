'''
Created on May 15, 2018

@author: jahre
'''

from calplotModules import fatal, NO_DATA_STRING

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