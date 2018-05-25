
import unittest
from calplotCore.io import readFilesForMerge
from calmerge import mergeData, processData, normaliseData
from calplotCore import isFloat

class Test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def compare(self, processedData, correctData):
        self.assertEqual(len(processedData), len(correctData), "Number of lines in the files should be equal")
        for i in range(len(processedData)):
            self.assertEqual(len(processedData[i]), len(correctData[i]), "Number of elements in each line should be equal")
            for j in range(len(processedData[i])):
                self.assertEqual(processedData[i][j], correctData[i][j], "Elements "+processedData[i][j]+" and "+correctData[i][j]+" are not equal")

    def testNormalization(self):
        fileData = readFilesForMerge(["calplotTest/merge-test-input.txt"], "\s+", "", False)
        mergedData, columnToFileList = mergeData(fileData, False, True)
        processedData, justify = processData(mergedData, [], "")
        processedData, justify = normaliseData(processedData, justify, 1, 2)

        correctData = readFilesForMerge(["calplotTest/merge-test-output.txt"], "\s+", "", False)
        mergedCorrectData, columnToFileList = mergeData(correctData, False, True)
        processedCorrectData, justify = processData(mergedCorrectData, [], "")
        
        self.compare(processedData, processedCorrectData)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()