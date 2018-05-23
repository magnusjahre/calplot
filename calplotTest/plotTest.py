'''
Created on May 16, 2018

@author: jahre
'''
import unittest
from calplotCore.io import readDataFile, createDataSeries
from calplotCore.plot import scatterPlot, plotLines, boxPlot, violinPlot, barChart

class Test(unittest.TestCase):


    def setUp(self):
        f = open("calplotTest/data.txt")
        self.header, data = readDataFile(f, "", "")
        f.close()
        
        self.dataseries = createDataSeries(data, len(self.header), "", False, False)
        self.outfile = "data.pdf"

    def tearDown(self):
        pass

    def testScatterPlot(self):
        scatterPlot(self.dataseries[1], self.dataseries[2], legend=self.dataseries[0], filename=self.outfile)

    def testLinePlot(self):
        plotLines(self.dataseries[0], self.dataseries[1:], titles=self.header, filename=self.outfile)
    
    def testBoxPlot(self):
        boxPlot(self.dataseries[1:], titles=self.header, filename=self.outfile)
    
    def testViolinPlot(self):
        violinPlot(self.header, self.dataseries[1:], filename=self.outfile)

    def testBarChart(self):
        barChart(self.dataseries[0], self.dataseries[1:], self.header, filename=self.outfile)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()