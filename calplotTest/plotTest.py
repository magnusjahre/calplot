'''
Created on May 16, 2018

@author: jahre
'''
import unittest
import os
from calplotCore.io import readDataFile, createDataSeries
from calplotCore.plot import scatterPlot, plotLines, boxPlot, violinPlot, barChart


class Test(unittest.TestCase):
    def getDataSeries(self, filename):
        f = open(filename)
        header, data = readDataFile(f, "", "")
        f.close()
        return header, createDataSeries(data, len(header), "", False, False)

    def getOutpath(self, name):
        return f"{self.outdir}/{name}"

    def setUp(self):
        self.header, self.dataseries = self.getDataSeries("calplotTest/testfiles/data.txt")
        self.missingDataHeader, self.missingDataSeries = self.getDataSeries("calplotTest/testfiles/missing-data.txt")
        self.outdir = "testplots"
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)

    def tearDown(self):
        pass

    def testScatterPlot(self):
        scatterPlot(self.dataseries[1], self.dataseries[2], legend=self.dataseries[0], filename=self.getOutpath("scatter.pdf"))

    def testLinePlot(self):
        plotLines(self.dataseries[0], self.dataseries[1:], titles=self.header, filename=self.getOutpath("lines.pdf"))

    def testLinePlotWithMissingData(self):
        plotLines(self.missingDataSeries[0], self.missingDataSeries[1:], titles=self.missingDataHeader, filename=self.getOutpath("lines-missing.pdf"))

    def testBoxPlot(self):
        boxPlot(self.dataseries[1:], titles=self.header, filename=self.getOutpath("box.pdf"))

    def testViolinPlot(self):
        violinPlot(self.header, self.dataseries[1:], filename=self.getOutpath("violin.pdf"))

    def testBarChart(self):
        barChart(self.dataseries[0], self.dataseries[1:], self.header, filename=self.getOutpath("bars.pdf"))

    def testBarChartWithMissingData(self):
        barChart(self.missingDataSeries[0], self.missingDataSeries[1:], self.missingDataHeader, filename=self.getOutpath("bars-missing.pdf"))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
