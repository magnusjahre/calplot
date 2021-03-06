
import unittest
from calplotCore.io import readFilesForMerge
from calmerge import mergeData, processData, normaliseData


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
                self.assertEqual(processedData[i][j], correctData[i][j], f"Elements {processedData[i][j]} and {correctData[i][j]} are not equal")

    def testNormalization(self):
        fileData = readFilesForMerge(["calplotTest/testfiles/merge-test-input.txt"], "\s+", "", False)
        mergedData, columnToFileList = mergeData(fileData, False, True)
        processedData, justify = processData(mergedData, [], "", False)
        processedData, justify = normaliseData(processedData, justify, "1", 2)

        correctData = readFilesForMerge(["calplotTest/testfiles/merge-test-output.txt"], "\s+", "", False)
        mergedCorrectData, columnToFileList = mergeData(correctData, False, True)
        processedCorrectData, justify = processData(mergedCorrectData, [], "", False)

        self.compare(processedData, processedCorrectData)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
