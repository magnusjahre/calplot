import math
from calplotModules import numberToString

###############################################################################
## Convenience methods
###############################################################################

def flip(items, ncol):
    tmp = [items[i::ncol] for i in range(ncol)]
    
    newitems = []
    for t in tmp:
        newitems += t
    
    return newitems

def addLegend(ax, plottedItems, legendNames, kwargs):

    useCols = 2
    if "legendColumns" in kwargs:
        if kwargs["legendColumns"] > 0:
            useCols = kwargs["legendColumns"]
        else:
            return
    
    if "mode" in kwargs:
        lmode = kwargs["mode"]
    else:
        lmode = "expand"
    
    bboxHeight = 0.115
    numRows = float(len(legendNames)) / useCols
    if numRows > 1.0:
        legendNames = flip(legendNames, useCols)
        plottedItems = flip(plottedItems, useCols)
        
        if "legendBBoxHeight" in kwargs:
            if kwargs["legendBBoxHeight"] == 0.0:
                bboxHeight = bboxHeight * math.ceil(numRows)
            else:
                bboxHeight = kwargs["legendBBoxHeight"]
        else:
            bboxHeight = bboxHeight * math.ceil(numRows)
            if lmode == "expand":
                bboxHeight = 0.3
        
    ax.legend(plottedItems, legendNames, bbox_to_anchor=(0.0, 1.04, 1.0, bboxHeight), loc="center", mode=lmode, borderaxespad=0.0,
              frameon=False, ncol=useCols, handletextpad=0.3, labelspacing=0.15, columnspacing=0.5)

###############################################################################
## Plot methods
###############################################################################

def scatterPlot(xdata, ydata, **kwargs):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.markers import MarkerStyle

    fontsize = 12
    width = 16
    height = 3.5
            
    if "figheight" in kwargs:
        height = kwargs["figheight"]  
    
    if "figwidth" in kwargs:
        width = kwargs["figwidth"] 
        fontsize = 14
    
    if "largeFonts" in kwargs:
        if kwargs["largeFonts"]:
            fontsize += 4
            
    matplotlib.rc('ps', useafm=True)
    matplotlib.rc('pdf', use14corefonts=True)
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('xtick', labelsize=fontsize) 
    matplotlib.rc('ytick', labelsize=fontsize)
    matplotlib.rc('legend', fontsize=fontsize)
    matplotlib.rc('font', size=fontsize)
    
    fig = plt.figure(figsize=(width,height))
    ax = fig.add_subplot(111)
    
    if(len(xdata) != len(ydata)):
        raise Exception("X and Y series data must be of equal length")
    
    scatters = []
    assert len(xdata) == len(ydata)
    for i in range(len(xdata)):
        thisColor = cm.Blues(1*(float(i)/len(xdata)))
        thisMarker = MarkerStyle.filled_markers[i % len(MarkerStyle.filled_markers)]
        scatters.append(ax.scatter(xdata[i], ydata[i], marker=thisMarker, color=thisColor, edgecolors="black"))
    
    if "xlabel" in kwargs:
        if kwargs["xlabel"] != "none":
            ax.set_xlabel(kwargs["xlabel"])
    if "ylabel" in kwargs:
        if kwargs["ylabel"] != "none":
            ax.set_ylabel(kwargs["ylabel"])
        
    if "yrange" in kwargs:
        if kwargs["yrange"] != None:
            try:
                yrange = kwargs["yrange"].split(",")
                ymin = float(yrange[0])
                ymax = float(yrange[1])
            except:
                raise Exception("Invalid yrange string")
            ax.set_ylim(ymin, ymax)
            
    if "xrange" in kwargs:
        if kwargs["xrange"] != "":
            try:
                xrange = kwargs["xrange"].split(",")
                xmin = float(xrange[0])
                xmax = float(xrange[1])
            except:
                raise Exception("Invalid xrange string")
            ax.set_xlim(xmin, xmax)
    
    addLegend(ax, scatters, kwargs["legend"], kwargs)
    
    if "title" in kwargs:
        if kwargs["title"] != "none":
            plt.text(0.5, 0.9, kwargs["title"],
                     horizontalalignment='center',
                     fontsize="large",
                     transform = ax.transAxes)
            
    if "vseparators" in kwargs:
        if kwargs["vseparators"] != "":
            coords = [float(i) for i in kwargs["vseparators"].split(",")]
            for c in coords:
                ax.axvline(x=c, linestyle="dashed")
                
    if "hseparators" in kwargs:
        if kwargs["hseparators"] != "":
            coords = [float(i) for i in kwargs["hseparators"].split(",")]
            for c in coords:
                ax.axhline(y=c, linestyle="dashed")
    
    
    if "filename" in kwargs:
        if kwargs["filename"] != None:
            plt.savefig(kwargs["filename"], type="pdf", bbox_inches='tight')
            return
    
    plt.show()

def plotLines(xvalues, ydataseries, **kwargs):
    
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib.markers import MarkerStyle
    
    fontsize = 12    
    width = 16
    height = 3.5
            
    if "figwidth" in kwargs:
        width = kwargs["figwidth"] 
        fontsize = 14
            
    if "largeFonts" in kwargs:
        if kwargs["largeFonts"]:
            fontsize += 4
    
    if "figheight" in kwargs:
        height = kwargs["figheight"] 
    
    matplotlib.rc('ps', useafm=True)
    matplotlib.rc('pdf', use14corefonts=True)
    if "notex" not in kwargs:
        matplotlib.rc('text', usetex=True)
    matplotlib.rc('xtick', labelsize=fontsize) 
    matplotlib.rc('ytick', labelsize=fontsize)
    matplotlib.rc('legend', fontsize=fontsize)
    matplotlib.rc('font', size=fontsize)
    
    fig = plt.figure(figsize=(width,height))
    ax = fig.add_subplot(111)
    
    plt.axhline(0, color='black')
    
    markEvery = 1
    if "markEvery" in kwargs:
        markEvery = kwargs["markEvery"]
    
    if "divFactor" in kwargs:
        for i in range(len(ydataseries)):
            for j in range(len(ydataseries[i])):
                ydataseries[i][j] = ydataseries[i][j] / kwargs["divFactor"]
    
    lines = []
    for i in range(len(ydataseries)):
        thisColor = cm.Paired(1*(float(i)/float(len(ydataseries))))
        thisMarker = MarkerStyle.filled_markers[i]
        lines += ax.plot(xvalues, ydataseries[i], color=thisColor, marker=thisMarker, markevery=markEvery)
    
    labels = None
    if "titles" in kwargs:
        if len(kwargs["titles"]) != len(ydataseries):
            raise Exception("The titles list must have the same length as the y-datalist list")
        
        labels = kwargs["titles"]
        for i in range(len(labels)):
            labels[i] = labels[i].replace("_"," ")
        
        addLegend(ax, lines, labels, kwargs)

    rotation = "horizontal"
    if "rotate" in kwargs:
        rotation = kwargs["rotate"]

    if rotation != "horizontal":
        ax.set_xticklabels([int(i) for i in ax.get_xticks()], rotation=rotation)
        ax.set_yticklabels([int(i) for i in ax.get_yticks()])

    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])
    
    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"])
       
    if "yrange" in kwargs:
        if kwargs["yrange"] != None:
            try:
                minval,maxval = kwargs["yrange"].split(",")
                minval = float(minval)
                maxval = float(maxval)
            except:
                raise Exception("Could not parse yrange string "+str(kwargs["yrange"]))    
            plt.ylim(minval,maxval)
            
            
    if "xrange" in kwargs:
        if kwargs["xrange"] != None:
            try:
                minval,maxval = kwargs["xrange"].split(",")
                minval = float(minval)
                maxval = float(maxval)
            except:
                raise Exception("Could not parse xrange string "+str(kwargs["xrange"]))    
            plt.xlim(minval,maxval)
    
    if "figtitle" in kwargs:
        if kwargs["figtitle"] != "none":
            plt.text(0.5, 0.9, kwargs["figtitle"],
                     horizontalalignment='center',
                     fontsize="large",
                     transform = ax.transAxes)
            
    if "separators" in kwargs:
        if kwargs["separators"] != "":
            coords = [float(i) for i in kwargs["separators"].split(",")]
            for c in coords:
                ax.axvline(x=c, linestyle="dashed")
                
    if "labels" in kwargs:
        if kwargs["labels"] != "":
            labelstr = [i for i in kwargs["labels"].split(":")]
            for t in labelstr:
                x,y,text,rotation = t.split(",")
                ax.text(float(x),float(y),text,rotation=rotation)
    
    if "fillBackground" in kwargs:
        if kwargs["fillBackground"] != "":
            labelstr = [i for i in kwargs["fillBackground"].split(":")]
            for t in labelstr:
                x1,x2 = t.split(",")
                ax.axvspan(float(x1),float(x2), color='lightgrey', linestyle=None, zorder=0.5)
    
    if "filename" in kwargs:
        if kwargs["filename"] != None:
            plt.savefig(kwargs["filename"], type="pdf", bbox_inches='tight')
            return
        
    plt.show()

""" Boxplot supports the following string parameters:
    - data: a list of lists containing the data ranges to be visualized

    - hideOutliers: shows/hides scatterplot of outliers
    - filename: write plot to this file
    - xlabel: x-axis label
    - ylabel: y-axis label
    - titles: A list of x-axis titles which contains the same number of elements
              as the data list
"""    
def boxPlot(data, **kwargs):
    
    import numpy as np
    import matplotlib
    
    fontsize = 10
    matplotlib.rc('xtick', labelsize=fontsize) 
    matplotlib.rc('ytick', labelsize=fontsize)
    matplotlib.rc('font', size=fontsize)
    
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import boxplot
    
    if "hideOutliers" in kwargs:
        if kwargs["hideOutliers"]:
            outSymbol = ""
        else:
            outSymbol = "b+"
    else:
        outSymbol = "b+"
    
    fig = plt.figure(figsize=(8,3))
    ax = fig.add_subplot(111)
    
    boxplot(data, sym=outSymbol)

    xPositions = [i for i in range(len(data)+1)[1:]] 
    averages = [np.average(d) for d in data]
    avgLine = plt.plot(xPositions, averages, 'o')

    if "titles" in kwargs:
        if len(kwargs["titles"]) != len(data):
            raise Exception("The titles list must have the same length as the data list")
  
        ax.set_xticklabels(kwargs["titles"], rotation="vertical")
    ax.set_xlim(0.5, len(data)+0.5)

    if "rotate" in kwargs:
        for label in ax.get_xticklabels():
            label.set_rotation(kwargs["rotate"])
        
    if "plotmargins" in kwargs:
        if kwargs["plotmargins"] != None:
            left,right,top,bottom = kwargs["plotmargins"] 
            plt.subplots_adjust(left=left, right=right, top=top, bottom=bottom)

    fig.legend(avgLine, ["Arithmetic Mean"], "upper center", numpoints=1)
    
    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])
    
    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"])
    
    if "filename" in kwargs:
        if kwargs["filename"] != None:
            plt.savefig(kwargs["filename"], type="pdf", bbox_inches='tight')
            return
    
    plt.show()

def violinPlot(names, values, **kwargs):
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm
    
    fontsize = 12
    width = 16
    height = 3.5
            
    if "figheight" in kwargs:
        height = kwargs["figheight"]  
    
    if "figwidth" in kwargs:
        width = kwargs["figwidth"] 
        fontsize = 14
    
    if "largeFonts" in kwargs:
        if kwargs["largeFonts"]:
            fontsize += 4
            
    matplotlib.rc('ps', useafm=True)
    matplotlib.rc('pdf', use14corefonts=True)
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('xtick', labelsize=fontsize) 
    matplotlib.rc('ytick', labelsize=fontsize)
    matplotlib.rc('legend', fontsize=fontsize)
    matplotlib.rc('font', size=fontsize)
    
    fig = plt.figure(figsize=(width,height))
    ax = fig.add_subplot(111)
    
    violinWidth = 0.8
    edgePadding = (1-violinWidth)/2
    pos = range(len(names))
        
    violinData = ax.violinplot(values, pos, points=100, widths=violinWidth, showmeans=False,
                               showextrema=False, showmedians=True, bw_method=0.1)

    plt.setp(violinData['bodies'], facecolor=cm.Blues(0.9), edgecolor='black')
    plt.setp(violinData['cmedians'], edgecolor='black')
    # plt.setp(violinData['cmins'], edgecolor='black')
    # plt.setp(violinData['cmaxes'], edgecolor='black')
    # plt.setp(violinData['cbars'], edgecolor='black')

    ax.set_xlim((-violinWidth/2)-edgePadding, len(names)-(violinWidth/2)-edgePadding)
    ax.set_xticks(pos)
    
    rotation = "horizontal"
    if "rotate" in kwargs:
        rotation = kwargs["rotate"]
    
    ax.set_xticklabels(names, rotation=rotation)
    ax.tick_params(axis="x", direction="out", top="off")
    
    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])
    
    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"], multialignment='center')
    
    if "yrange" in kwargs:
        if kwargs["yrange"] != None:
            try:
                miny,maxy = kwargs["yrange"].split(",")
                miny = float(miny)
                maxy = float(maxy)
            except:
                raise Exception("Could not parse yrange string "+str(kwargs["yrange"]))    
            plt.ylim(miny,maxy)
    
    if "labels" in kwargs:
        if kwargs["labels"] != "":
            labelstr = [i for i in kwargs["labels"].split(":")]
            for t in labelstr:
                x,y,text = t.split(",")
                ax.text(float(x),float(y),text)
    
    if "filename" in kwargs:
        if kwargs["filename"] != None:
            plt.savefig(kwargs["filename"], type="pdf", bbox_inches='tight')
            return
    plt.show()

def barChart(names, values, legendNames, **kwargs):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm

    fontsize = 12
    width = 16
    height = 3.5
            
    if "figheight" in kwargs:
        height = kwargs["figheight"]  
    
    if "figwidth" in kwargs:
        width = kwargs["figwidth"] 
        fontsize = 14
    
    if "largeFonts" in kwargs:
        if kwargs["largeFonts"]:
            fontsize += 4
            
    matplotlib.rc('ps', useafm=True)
    matplotlib.rc('pdf', use14corefonts=True)
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('xtick', labelsize=fontsize) 
    matplotlib.rc('ytick', labelsize=fontsize)
    matplotlib.rc('legend', fontsize=fontsize)
    matplotlib.rc('font', size=fontsize)
    

    fig = plt.figure(figsize=(width,height))
    ax = fig.add_subplot(111)
    width = 0.8

    for i in range(len(names)):
        names[i] = names[i].replace("_"," ")

    for i in range(len(legendNames)):
        legendNames[i] = legendNames[i].replace("_"," ")

    errorcols = False
    if "errorcols" in kwargs:
        errorcols = kwargs["errorcols"]
        if errorcols:
            if len(values) % 2 != 0:
                raise Exception("Columns must be a multiple of 2 to plot errorcols")

    errorrows = False
    if "errorrows" in kwargs:
        errorrows = kwargs["errorrows"]
        if errorrows:
            errordata = []
            newvalues = []
            for i in range(len(values)):
                errordata.append([])
                newvalues.append([])
                for j in range(len(values[i]))[1::2]:
                    errordata[i].append(values[i][j])
                    newvalues[i].append(values[i][j-1])
                    
            values = newvalues
                
    if errorcols:
        numSeries = len(values)/2
        localLegend = []
    else:
        numSeries = len(values)
        localLegend = legendNames
        
        if errorrows:
            newnames = names[0::2]
            names = newnames
    
    ind = np.arange(len(names))+0.1
    
    bars = []
    for i in range(numSeries):
        barwidth = width/float(numSeries)
        thisColor = cm.Blues(1*(float(i)/numSeries))
        if errorcols:
            bars.append(ax.bar(ind+(barwidth*i), values[2*i], barwidth, yerr=values[(2*i)+1], ecolor="black", color=thisColor))
            localLegend.append(legendNames[2*i])
        elif errorrows:
            bars.append(ax.bar(ind+(barwidth*i), values[i], barwidth, yerr=errordata[i], ecolor="black", color=thisColor))
        else:
            bars.append(ax.bar(ind+(barwidth*i), values[i], barwidth, color=thisColor))
        
    ax.set_xlim(0, len(names))
    ax.set_xticks(ind+(width/2.0))
         
    rotation = "horizontal"
    if "rotate" in kwargs:
        rotation = kwargs["rotate"]
    
    ax.set_xticklabels(names, rotation=rotation)
    
    plt.axhline(0, color='black')
    
    addLegend(ax, bars, localLegend, kwargs)  
    
    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])
    
    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"], multialignment='center')
    
    ymax = -1
    if "yrange" in kwargs:
        if kwargs["yrange"] != None:
            try:
                miny,maxy = kwargs["yrange"].split(",")
                miny = float(miny)
                maxy = float(maxy)
            except:
                raise Exception("Could not parse yrange string "+str(kwargs["yrange"]))    
            plt.ylim(miny,maxy)
            ymax = maxy
    
    if "datalabels" in kwargs:
        if kwargs["datalabels"] != "":
            for datalabel in kwargs["datalabels"].split(":"):
                try:
                    labelvalues = datalabel.split(",")
                    seriesindex = int(labelvalues[0])
                    itemindex = int(labelvalues[1])
                    decimals = int(labelvalues[2])
                except:
                    raise Exception("Could not parse datalabel string "+datalabel)
                
                yoffset = 100
                if ymax != -1:
                    yoffset = 0.02 * ymax
                
                for i in range(len(values)):
                    xcoords = ind+(barwidth*i)+(0.5*barwidth)
                    for j in range(len(xcoords)):
                        if i == seriesindex and j == itemindex:
                            plt.text(xcoords[j], yoffset, numberToString(values[i][j], decimals), rotation="vertical", ha="center", va="bottom")

    
    if "separators" in kwargs:
        if kwargs["separators"] != "":
            coords = [float(i) for i in kwargs["separators"].split(",")]
            for c in coords:
                ax.axvline(x=c, linestyle="dashed")
    
    if "linemarkers" in kwargs:
        if kwargs["linemarkers"] != "":
            coords = [float(i) for i in kwargs["linemarkers"].split(",")]
            for c in coords:
                ax.axhline(y=c)
    
    if "labels" in kwargs:
        if kwargs["labels"] != "":
            labelstr = [i for i in kwargs["labels"].split(":")]
            for t in labelstr:
                x,y,text,rotation = t.split(",")
                ax.text(float(x),float(y),text,rotation=rotation)
                
    if "fillBackground" in kwargs:
        if kwargs["fillBackground"] != "":
            labelstr = [i for i in kwargs["fillBackground"].split(":")]
            for t in labelstr:
                x1,x2 = t.split(",")
                ax.axvspan(float(x1),float(x2), color='lightgrey', linestyle=None, zorder=0.5)
    
    if "filename" in kwargs:
        if kwargs["filename"] != None:
            plt.savefig(kwargs["filename"], type="pdf", bbox_inches='tight')
            return
    plt.show()
