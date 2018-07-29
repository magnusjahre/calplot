# Calplot

This repository contains a frontend to matplotlib for plotting figures for papers that is used at NTNU's Computer Architecture Lab. It has two primary use cases:
 * Using the commandline interface to quickly plot experimental data while working
 * Integration with SCons for plotting highly optimized figures for papers

Although Calplot in theory should be cross-platform, it is currently only tested on Linux and OSX.
 
## Setting up Calplot

For the scripts to work, you must first install:
 * Python version 2.7 or newer (Note that calplot does not work with Python version 3)
 * Matplotib (https://matplotlib.org)
 * Latex
 * Git

For Ubuntu 18.04, first open a terminal. Then run the following commandline to install all prerequisites:
```
sudo apt-get install python python-matplotlib texlive git
```

Then, clone calplot using the following command:
```
git clone https://github.com/magnusjahre/calplot.git
```

In addition, you need to add the calplot root directory to the *PYTHONPATH* environment variable. Adding the following to \~/.bashrc on Linux (\~/.bash_profile on Mac OS\) and restarting the terminal will do the trick:
```
export CALPLOTPATH=[INSERT_CALPLOT_PATH_HERE]/calplot
export PYTHONPATH=$PYTHONPATH:$CALPLOTPATH
```

Finally, enter the calplot directory and run the tests to verify that the scripts work as intended:
```
cd calplot
./runTests.sh
```

## Using Calplot

The basic operation is as follows:
 * The user provides one or more datafiles. An example datafile can be found in the calplotTest directory.
 * If necessary, the user uses the calmerge.py script to modify the datafile (e.g., normailization). For complex operations, it may be helpful to call calmerge.py multiple times.
 * The user uses calplot.py to plot the datafile.
 
Both calmerge.py and calplot.py have a large number of option which will be printed when the --help option is provided.

# SCons integration

For SCons integration to work, SCons needs to know where to find calplot. To make this work, you need to set the *CALPLOTPATH* environment variable to contain the absolute path to the calplot repository. If you followed the setup instructions above to the letter, you will already have set *CALPLOTPATH* correctly.

The code below sets up the methods needed.

```python

import os
import sys
from subprocess import call

if "CALPLOTPATH" not in os.environ:
    print "ERROR: Path to calplot script is not available. Make sure environment variable CALPLOTPATH is available"
    sys.exit()

scriptroot = os.environ["CALPLOTPATH"]
if scriptroot not in sys.path:
    sys.path.append(scriptroot)
if "PYTHONPATH" not in os.environ:
    os.environ["PYTHONPATH"] = scriptroot

from calmerge import generateMergeCommand
from calplot import generatePlotCommand
```
Calplot contains convenience methods that call calplot.py and calmerge.py with correct parameters when provided with a dictionary following a specific format. The format matches the options provided by calmerge and calplot.

```python
merges = []
plots = []

merges.append({"files": ["plots/cores-vs-s-energy-data.txt"],
               "outfile": "plots/cores-vs-s-energy-data-norm.txt",
               "colnames": "",
               "rownames": "",
               "opts": ["--normalize-to", "10", "--no-color"]})
 
plots.append({"input": "plots/cores-vs-s-energy-data-norm.txt",
              "output": "plots/cores-vs-s-energy-data-norm.pdf",
              "type": "bars",
              "ytitle": "Relative Energy",
              "xtitle": 'Number of Cores',
              "opts": ["--legend-columns", "5", "--yrange", "0,1.25"] + getDimensions(2)})

for m in merges:
    env.Command(m["outfile"], m["files"], "python "+scriptroot+"/"+generateMergeCommand(m))

plotDeps = []
for p in plots:
    plotDeps.append(env.Command(p["output"], p["input"], "python "+scriptroot+"/"+generatePlotCommand(p)))

paper = env.PDF(mainfile)

Depends(paper, plotDeps)
```
