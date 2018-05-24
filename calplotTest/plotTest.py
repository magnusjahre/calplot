'''
Created on May 16, 2018

@author: jahre
'''
import unittest
from calplotCore.io import readDataFile, createDataSeries
from calplotCore.plot import scatterPlot, plotLines, boxPlot, violinPlot, barChart

class Test(unittest.TestCase):


    def getDataSeries(self, filename):
        f = open(filename)
        header, data = readDataFile(f, "", "")
        f.close()
        return header, createDataSeries(data, len(header), "", False, False)

    def setUp(self):
        self.header, self.dataseries = self.getDataSeries("calplotTest/data.txt")
        self.missingDataHeader, self.missingDataSeries = self.getDataSeries("calplotTest/missing-data.txt")
        self.outfile = "data.pdf"

    def tearDown(self):
        pass

    def testScatterPlot(self):
        scatterPlot(self.dataseries[1], self.dataseries[2], legend=self.dataseries[0], filename=self.outfile)

    def testLinePlot(self):
        plotLines(self.dataseries[0], self.dataseries[1:], titles=self.header, filename=self.outfile)

    def testLinePlotWithMissingData(self):
        plotLines(self.missingDataSeries[0], self.missingDataSeries[1:], titles=self.missingDataHeader, filename=self.outfile)
    
    def testBoxPlot(self):
        boxPlot(self.dataseries[1:], titles=self.header, filename=self.outfile)
    
    def testViolinPlot(self):
        violinPlot(self.header, self.dataseries[1:], filename=self.outfile)

    def testBarChart(self):
        barChart(self.dataseries[0], self.dataseries[1:], self.header, filename=self.outfile)

    def testBarChartWithMissingData(self):
        barChart(self.missingDataSeries[0], self.missingDataSeries[1:], self.missingDataHeader, filename=self.outfile)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()