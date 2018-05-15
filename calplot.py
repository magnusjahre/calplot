#!/usr/bin/env python

'''
Created on May 15, 2018

@author: jahre
'''

from optparse import OptionParser
from calplotModules import fatal, NO_DATA_STRING
from calplotModules.io import readDataFile

from calplotModules.plot import boxPlot, plotLines, barChart, violinPlot, scatterPlot

def parseArgs():
    parser = OptionParser(usage="calplot.py [options] filename [filename ...]")

    plotTypes = ["boxes", "lines", "bars", "violin", "scatter"]

    parser.add_option("--quiet", action="store_true", dest="quiet", default=False, help="Only write results to stdout")
    parser.add_option("--decimals", action="store", dest="decimals", type="int", default=2, help="Number of decimals to use when printing results")
    parser.add_option("--legend-columns", action="store", dest="legendColumns", type="int", default=2, help="Number of columns in legend")
    parser.add_option("--legend-bbox-height", action="store", dest="legendBBoxHeight", type="float", default=0.0, help="Manually set the height of the bbox legend to this value.")
    parser.add_option("--margins", action="store", dest="margins", type="string", default="", help="Comma separated plot margins: left,right,top,bottom ")
    parser.add_option("--outfile", action="store", dest="outfile", type="string", default=None, help="Output filename (Default: plot.pdf)")
    parser.add_option("--plot-type", action="store", dest="plotType", type="string", default="bars", help="Output filename (Default: bars, alternatives "+str(plotTypes)+")")
    parser.add_option("-y", "--ytitle", action="store", dest="ytitle", type="string", default="Y axis title", help="Y axis title")
    parser.add_option("-x", "--xtitle", action="store", dest="xtitle", type="string", default="X axis title", help="X axis title")
    parser.add_option("--yrange", action="store", dest="yrange", type="string", default=None, help="Comma separated min,max pair")
    parser.add_option("--xrange", action="store", dest="xrange", type="string", default=None, help="Comma separated min,max pair")
    parser.add_option("--columns", action="store", dest="columns", type="string", default="", help="Comma separated list of columns to include (Zero indexed)")
    parser.add_option("--errorrows", action="store_true", dest="errorrows", default=False, help="Every second row in the data file is error values")
    parser.add_option("--errorcols", action="store_true", dest="errorcols", default=False, help="Every second column in the data file is error values")
    parser.add_option("--only-type", action="store", dest="onlyType", type="string", default="", help="Only include lines that have a workload key that contains this letter (a, b, c or n)")
    parser.add_option("--avg", action="store_true", dest="avg", default=False, help="Add average as a part of the data set")
    parser.add_option("--fix-wls", action="store_true", dest="fixWls", default=False, help="Improve the readability of workload names")
    parser.add_option("--only-wl-num", action="store_true", dest="onlyWlNum", default=False, help="Only show the workload number")
    parser.add_option("--figure-height", action="store", dest="figheight", type="float", default=3.5, help="Plot with custom height")
    parser.add_option("--figure-width", action="store", dest="figwidth", type="float", default=16.0, help="Plot with custom width")
    parser.add_option("--rotate", action="store", dest="rotate", type="string", default="horizontal", help="Rotate the x-axis captions")
    parser.add_option("--datalabels", action="store", dest="datalabels", type="string", default="", help="Show data values on selected bars (Format: seriesindex,valueindex,decimals[: ... ])")
    parser.add_option("--mark-every", action="store", dest="markEvery", type="int", default=1, help="Mark every nth data point in a line plot (default is 1)")
    parser.add_option("--large-fonts", action="store_true", dest="largeFonts", default=False, help="Increase the font size (useful for really small plots)")
    parser.add_option("--div-factor", action="store", dest="divFactor", type="float", default=1.0, help="Divide all y values by this constant")
    parser.add_option("--mode", action="store", dest="mode", type="string", default="expand", help="The mode of the legend, set to None to disable expansion")
    parser.add_option("--separators", action="store", dest="separators", type="string", default="", help="Add separator lines at these x-values, comma separated")
    parser.add_option("--linemarkers", action="store", dest="linemarkers", type="string", default="", help="Add line markers at these y-values, comma separated")
    parser.add_option("--labels", action="store", dest="labels", type="string", default="", help="Add labels  at these coordinates, x,y,text,rotation[:x,y,text,rotation]")
    parser.add_option("--fill-background", action="store", dest="fillBackground", type="string", default="", help="Fill the background between x-ranges x1,x2[:xi,yj]")

    opts, args = parser.parse_args()
    
    datafiles = []
    for a in args:
        try:
            datafiles.append(open(a))
        except:
            try:
                fatal("Cannot open file "+str(a))
            except:
                print parser.usage
                fatal("Command line error")
    
    if datafiles == []:
        fatal("The name of at least one data file needs to be supplied")
    
    if opts.plotType not in plotTypes:
        fatal("Plot type needs to be one of "+str(plotTypes))
    
    if opts.plotType != "boxplot" and len(datafiles) > 1:
        fatal("Plotting of multiple data files only make sense for boxplots")
    
    return opts, args, datafiles

def createDataSeries(rawdata, datacols, opts):
    dataseries =[[] for i in range(datacols+1)]
    
    for l in rawdata:
        for i in range(datacols+1):
            if opts.plotType == "scatter":
                dataseries[i].append(l[i])
            elif l[i] != NO_DATA_STRING:
                dataseries[i].append(l[i])

    if opts.fixWls:
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
        
    if opts.onlyWlNum:
        newWls = []
        for wl in dataseries[0]:
            tmp = wl.split("-")
            newWls.append(tmp[-1])
        
        dataseries[0] = newWls

    return dataseries

def generatePlotCommand(data):
    cmd = ["plotDataFile.py"]
    cmd.append("--plot-type")
    cmd.append(data["type"])
    cmd.append("-y")
    cmd.append('"'+data["ytitle"]+'"')
    cmd.append("-x")
    cmd.append('"'+data["xtitle"]+'"')
    for o in data["opts"]:
        cmd.append(o)

    cmd.append("--outfile")
    cmd.append(data["output"])
    cmd.append(data["input"])
    
    return " ".join(cmd)

def getScatterData(dataseries):
    xdata = [[] for i in range(len(dataseries)-1)]
    ydata = [[] for i in range(len(dataseries)-1)]
    
    for i in range(len(dataseries[1:])):
        for j in range(len(dataseries[0])):
            if dataseries[i+1][j] != NO_DATA_STRING:
                xdata[i].append(dataseries[0][j])
                ydata[i].append(dataseries[i+1][j])
                
    return xdata, ydata

def main():

    opts, args, datafiles = parseArgs()
    
    print "Data file plot script"
    
    dataseries = []
    header = []
    for i in range(len(datafiles)):
        print "Processing file plot of file "+args[i]
        
        thisHeader, thisData = readDataFile(datafiles[i], opts.columns, opts.onlyType)
        series = createDataSeries(thisData, len(thisHeader), opts)
        
        if opts.plotType != "boxes":
            dataseries = series
            header = thisHeader
        else:
            for s in series[1:]:
                dataseries.append(s)
                
            for h in thisHeader:
                header.append(h)
    
    if opts.avg:
        for i in range(len(dataseries)):
            if i == 0:
                dataseries[i].append("AVG")
            else:
                avg = float(sum(dataseries[i])) / float(len(dataseries[i]))
                dataseries[i].append(avg)
    
    if opts.margins != "":
        margList = opts.margins.split(",")
        try:
            margs = (float(margList[0]),float(margList[1]),float(margList[2]),float(margList[3]))
        except:
            fatal("Margin plot error")
    else:
        margs = None
    
    if opts.outfile != None:
        print "Plotting data to file "+opts.outfile+"..."
    else:
        print "Showing plot..."
    
    usemode = opts.mode
    if usemode == "None":
        usemode = None
    
    if opts.plotType == "lines":
        plotLines(dataseries[0], dataseries[1:],
                        titles=header,
                        filename=opts.outfile,
                        xlabel=opts.xtitle,
                        ylabel=opts.ytitle,
                        legendColumns=opts.legendColumns,
                        yrange=opts.yrange,
                        xrange=opts.xrange,
                        figheight=opts.figheight,
                        figwidth=opts.figwidth,
                        markEvery=opts.markEvery,
                        largeFonts=opts.largeFonts,
                        divFactor=opts.divFactor,
                        labels=opts.labels,
                        separators=opts.separators,
                        fillBackground=opts.fillBackground,
                        rotate=opts.rotate)
        
    elif opts.plotType == "bars":
        barChart(dataseries[0],
                             dataseries[1:],
                             header,
                             filename=opts.outfile,
                             xlabel=opts.xtitle,
                             ylabel=opts.ytitle,
                             legendColumns=opts.legendColumns,
                             legendBBoxHeight=opts.legendBBoxHeight,
                             yrange=opts.yrange,
                             errorrows=opts.errorrows,
                             errorcols=opts.errorcols,
                             rotate=opts.rotate,
                             datalabels=opts.datalabels,
                             figheight=opts.figheight,
                             figwidth=opts.figwidth,
                             mode=usemode,
                             separators=opts.separators,
                             linemarkers=opts.linemarkers,
                             labels=opts.labels,
                             fillBackground=opts.fillBackground)
    elif opts.plotType == "violin":
        violinPlot(header,
                   dataseries[1:],
                   filename=opts.outfile,
                   xlabel=opts.xtitle,
                   ylabel=opts.ytitle,
                   yrange=opts.yrange,
                   rotate=opts.rotate,
                   figheight=opts.figheight,
                   figwidth=opts.figwidth,
                   labels=opts.labels)
    
    elif opts.plotType == "scatter":
        xdata, ydata = getScatterData(dataseries)
        scatterPlot(xdata,
                       ydata,
                       legend=header,
                       filename=opts.outfile,
                       xlabel=opts.xtitle,
                       ylabel=opts.ytitle,
                       legendColumns=opts.legendColumns,
                       yrange=opts.yrange,
                       figheight=opts.figheight,
                       figwidth=opts.figwidth,
                       mode=usemode) 
    else:
        assert opts.plotType == "boxes"
        boxPlot(dataseries,
                       titles=header,
                       plotmargins=margs,
                       filename=opts.outfile,
                       xlabel=opts.xtitle,
                       ylabel=opts.ytitle)

    print "Done!"

if __name__ == '__main__':
    main()
