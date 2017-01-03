#!/usr/bin/env python


import sys
import os.path
import datetime
import pandas as pd
import numpy as np
from SphericalDistribution import SphericalDistribution


def main(argv):

	# print(datetime.datetime.now())
	# return
	# Output Syntax
	if len(argv) < 2:
		msg = "Syntax: python sphericalDistributionAnalysisKit.py "
		msg += "inputPath [--GenerateVisualizations=visualizationPath] "
		msg += "[--GenerateGraphs=graphPath] [--GenerateWaveFront] "
		msg += "[--MetricsOutput]"
		print(msg)
		return

	# Input path always first argument
	inputPath = argv[1]

	visualizationOutputPath = './Visualization/'
	outputPath = "./Metrics-Output.csv"
	graphsOutputPath = "./Graphs/"

	visualizationFlag = False
	graphFlag = False
	wavefrontFlag = False
	cleanDataFlag = False

	# Parse the input arguments
	for i in range(2, len(argv)):
		argPri = argv[i]
		argSec = None
		if i + 1 < len(argv):
			argSec = argv[i + 1]

		if argPri[0] is '-':
			if argPri[1] is 'o':
				if argSec is None or argSec[0] is '-':
					print('ERROR - Invalid output path')
					return
				outputPath = argSec
			elif argPri[1] is 'v':
				visualizationFlag = True
				if argSec is None or argSec[0] is '-':
					print('ERROR - Invalid visualization path')
					return
				visualizationOutputPath = argSec
			elif argPri[1] is 'g':
				graphFlag = True
				if argSec is None or argSec[0] is '-':
					print('ERROR - Invalid graph path')
					return
				graphsOutputPath = argSec
			elif argPri[1] is 'c':
				cleanDataFlag = True

	print("Input Path: {}".format(inputPath))
	print("Output Path: {}".format(outputPath))
	print("Visualization Path: {}".format(visualizationOutputPath))
	# print("Wavefront Path: {}".format(generateWaveFrontPath))
	

	metricData = None

	# If the clean data flag is set to true do not load data, we want to recalcuate
	# all metrics 
	if cleanDataFlag is False:
		metricData = loadExistingMetricData(outputPath)

	# Build recursive list of input files from the provided input path
	inputFiles = createInputFileList(inputPath, True)

	distributionDict = {}

	# Create a Spherical Distribution object for each input file
	for inputFilePath in inputFiles:

		# Create arguments dictionary and distribution object
		sdArgs = {}
		sdArgs['DataFilePath'] = inputFilePath
		sdArgs['RuntimeDataFilePath'] = inputFilePath + '-runtime'
		dist = SphericalDistribution(sdArgs)

		# Only add the distribution to the dictionary for processing if it doesn't
		# already exist in the dictionary
		if metricData is None or len(metricData[metricData['DataSetName'] == dist.DataSetName]) == 0:
			distributionDict[dist.DataSetName] = dist

	# Process each distributon in the dictionary, saving results to file
	for distKey in sorted(distributionDict.keys()):

		distName = distributionDict[distKey].DataSetName

		startTime = datetime.datetime.now()
		print("\t * Started processing distribution {} at {}".format(distName, startTime))

		# Load the distribution data and calculate the metrics
		distributionDict[distKey].loadData()
		distributionDict[distKey].calculateMetrics()

		# Output metrics to file after each distribution is processed
		metricData = addResultToMetrics(distributionDict[distKey], metricData)
		metricData.to_csv(outputPath)

		endTime = datetime.datetime.now()
		processTime = endTime - startTime
		print("\t * Finished processing distribution {} at {}....Processing time: {}".format(distName, endTime, processTime))


def createInputFileList(inputPath, recursiveSearch):
	inputFiles = []
	# If inputPath is directory iterate through each item
	if os.path.isdir(inputPath) is True:
		# Get 
		fileList = os.listdir(inputPath)
		fileList.sort()

		for file in fileList:
			filePath = os.path.join(inputPath, file)
			if os.path.isdir(filePath) is True and recursiveSearch is True:
				subInputFiles = createInputFileList(filePath, recursiveSearch)

				for subFile in subInputFiles:
					inputFiles.append(subFile)

			elif os.path.isfile(filePath) and "-runtime" not in filePath:
				inputFiles.append(filePath)
	elif os.path.isfile(inputPath) is True:
		inputFiles.append(inputPath)
	else:
		print("Error - inputPath is not a valid folder or file")
		return
	return inputFiles


def loadExistingMetricData(metricsPath):
	metricData = None

	if os.path.isfile(metricsPath):
		print("* Loading existing Metric data from {}".format(outputPath))
		metricData = pd.read_csv(metricsPath)
	else:
		print("* ERROR")
	return metricData


def addResultToMetrics(dist, metricData):

	resultArray = []
	resultArray.append("DataSetName")
	resultArray.append("NumPoints")
	resultArray.append("Iterations")
	resultArray.append("Method")
	resultArray.append("ExecutionNumber")
	resultArray.append("AverageRunTime")
	resultArray.append("ClocksPerSecond")
	resultArray.append("SeparationDistance")
	resultArray.append("CoveringRadius")
	resultArray.append("MeshSeparationRatio")

	# Create array of distribution results
	distResult = []
	distResult.append(dist.DataSetName)
	distResult.append(len(dist.Voronoi.points))
	distResult.append(dist.NumberIterations)
	distResult.append(dist.Method)
	distResult.append(dist.ExecutionNumber)
	distResult.append(dist.AverageRunTime)
	distResult.append(dist.ClocksPerSecond)
	distResult.append(dist.SeparationDistance)
	distResult.append(dist.CoveringRadius)
	distResult.append(dist.MeshSeparationRatio)

	# Create pandas dataframe from distribution result
	distData = pd.DataFrame([distResult], columns=resultArray)
	
	if metricData is None:
		return distData

	# Append the distribution data and return all metric data
	return metricData.append(distData)


if __name__ == '__main__':
	main(sys.argv)
