import sys
import os.path
import time
from SphericalDistribution import *

def main(argv):
	if len(argv) < 2:
		msg = "Syntax: python sphericalDistributionAnalysisKit.py "
		msg = msg + "inputPath [--GenerateVisualizations] [--GenerateGraphs]"
		print(msg)
		return

	inputFiles = []
	inputPath = argv[1]

	# Validate input path exists and get a list of files
	if os.path.isdir(inputPath) is True:
		fileList = os.listdir(inputPath)
		fileList.sort()
		for file in fileList:
			if os.path.isfile(os.path.join(inputPath, file)):
				inputFiles.append(os.path.join(inputPath, file))
	elif os.path.isfile(inputPath) is True:
		inputFiles.append(inputPath)
	else:
		print("Error - inputPath is not a valid folder or file")
		return

	visualizationOutputPath = None
	metricsOutputPath = "./Results/"
	graphsOutputPath = None

	for i in range(2, len(argv)):
		splitArg = argv[i].split('=')

		if len(splitArg) != 2:
			print("Error - invalid syntax at argument: " + argv[i])
			return

		if splitArg[0] == "--GenerateVisualizations":
			visualizationOutputPath = splitArg[1]
			continue

		if splitArg[0] == "--GenerateGraphs":
			graphsOutputPath = splitArg[1]
			continue

		if splitArg[0] == "--MetricsOutput":
			metricsOutputPath = splitArg[1]
			continue

	distributionArray = []

	for inputFilePath in inputFiles:
		startTime = time.clock()
		print("Start Processing: " + inputFilePath + " at " + str(startTime))
		dist = SphericalDistribution(inputFilePath)
		distributionArray.append(dist)
		endTime = time.clock()
		print("Finished Processing: " + inputFilePath + " at " + str(startTime))
		print("\t\tRun Time: " + str(endTime - startTime))



	outputData(distributionArray, metricsOutputPath)

def outputData(distributionArray, outputFolderPath):

	try:
		os.stat(outputFolderPath)
		# fileList = os.listdir(inputPath)
		# for file in fileList:
		# 	os.remove(file)
	except:
		os.mkdir(outputFolderPath)

	for dist in distributionArray:
		outputFilePath = outputFolderPath + dist.DataSetName + ".csv"
		outputLine = None

		if os.path.isfile(outputFilePath) is False:
			outputLine = dist.outputMetrics(True)
			outputFile = open(outputFilePath, "a")
			outputFile.write(outputLine + "\n")
		else:
			outputFile = open(outputFilePath, "a")

		outputLine = dist.outputMetrics(False)
		outputFile.write(outputLine + "\n")
		outputFile.close()



if __name__ == '__main__':
	main(sys.argv)
