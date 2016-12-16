import math
import numpy as np
import scipy.spatial


class SphericalDistribution:

	def __init__(self, args):
		
		self.Points = None
		self.Runtimes = None
		self.SeparationDistance = None
		self.PackingRadius = None
		self.CoveringRadius = None
		self.MeshSeparationRatio = None
		self.AverageRunTime = None
		self.ClocksPerSecond = None
		self.ExecutionNumber = None
		self.NumberIterations = None
		self.Method = None
		self.FileName = None
		self.DataSetName = None
		self.RuntimeInputFilePath = None
		self.Voronoi = None

		self.VerboseLevel = 0

		self.InputFilePath = args['DataFilePath']
		
		if 'RuntimeDataFilePath' in args.keys():
			self.RuntimeInputFilePath = args['RuntimeDataFilePath']

		loadData = False
		if 'LoadData' in args.keys() and args['LoadData'] is True:
			loadData = True

		calculateMetrics = False
		if 'CalculateMetrics' in args.keys() and args['CalculateMetrics'] is True:
			calculateMetrics = True

		self.parseDataSetName()
		if loadData:
			self.loadData()

			if calculateMetrics:
				self.calculateMetrics()

	
	def calculateMetrics(self):
		
		if self.Points is not None:
			self.Voronoi = scipy.spatial.SphericalVoronoi(self.Points)

			self.calculateSeparationDistance()
			self.calculatePackingRadius()
			self.calculateCoveringRadius()
			self.calculateMeshSeparationRatio()
			self.calculateAverageRunTime()


	def loadData(self):
		self.Points = np.genfromtxt(self.InputFilePath, delimiter=",")

		if self.RuntimeInputFilePath is not None:
			runTimeFile = open(self.RuntimeInputFilePath, "r")

			self.Runtimes = []
			for line in runTimeFile:
				line = line.strip(' \t\n\r')

				splitLine = line.split(",")

				if len(splitLine) > 1:
					self.Runtimes.append(splitLine)

	def vectorDotProduct(point1, point2):
		if len(point1) is not 3 or len(point2) is not 3:
			print("Error - Invalid points")
			return 0

		return point1[0] * point2[0] + point1[1] * point2[1] + point1[2] * point2[2]

	def haversineDistance(point1, point2):
		distance = 0

		if len(point1) is 3 or len(point2) is 3:
			dotProduct = SphericalDistribution.vectorDotProduct(point1, point2)

			if (dotProduct > 1):
				distance = 0
			elif (dotProduct < -1):
				distance = 100
			else:
				distance = math.acos(dotProduct)

		return distance


	def calculateSeparationDistance(self):
		minDistance = self.Circumference()

		for i in range(0, len(self.Voronoi.points)):
			for j in range(0, len(self.Voronoi.points)):
				if i != j:
					distance = SphericalDistribution.haversineDistance(self.Voronoi.points[i], self.Voronoi.points[j])

					if distance < minDistance:
						minDistance = distance

		self.SeparationDistance = minDistance

	def calculatePackingRadius(self):
		self.PackingRadius = self.SeparationDistance / 2

	def calculateCoveringRadius(self):
		coveringRadius = 0

		for i in range(0, len(self.Voronoi.vertices)):
			vert = self.Voronoi.vertices[i]

			vertRegions = []

			for j in range(0, len(self.Voronoi.regions)):
				if i in self.Voronoi.regions[j]:
					vertRegions.append(j)

			localMin = self.Circumference()

			for vr in vertRegions:
				p = self.Voronoi.points[vr]

				dist = SphericalDistribution.haversineDistance(p, vert)
				if dist < localMin:
					localMin = dist

			if localMin > coveringRadius:
				coveringRadius = localMin

		self.CoveringRadius = coveringRadius

	def calculateAverageRunTime(self):
		if self.Runtimes is None:
			self.AverageRunTime = -1
			return

		self.AverageRunTime = 0

		for runTime in self.Runtimes:
			self.AverageRunTime += float(runTime[3])


		self.AverageRunTime /= len(self.Runtimes)
		self.ClocksPerSecond = self.Runtimes[0][4]


	def Circumference(self):
		return 2 * math.pi * self.Voronoi.radius

	def calculateMeshSeparationRatio(self):
		self.MeshSeparationRatio = self.CoveringRadius / self.SeparationDistance

	def generateNDArray(self):
		if self.PointArray is None:
			print("No Points")
			return None

		ndArray = []

		for point in self.PointArray:
			ndArray.append([point.cartesian.x, point.cartesian.y, point.cartesian.z])

		ndArray = np.array(ndArray)
		return ndArray


	def outputMetrics(self, headerFlag):
		line = None

		if headerFlag is True:
			line = "DataSetName,NumPoints,Iterations,Method,ExecutionNumber,"
			line += "AverageRunTime,ClocksPerSecond,"
			line += "SeparationDistance,"
			line += "MeshNorm-CoveringRadius,MeshRatio-MeshSeparationRatio"
		else:
			line = self.DataSetName
			line += "," + str(len(self.Voronoi.points))
			line += "," + str(self.NumberIterations)
			line += "," + str(self.Method)
			line += "," + str(self.ExecutionNumber)
			line += "," + str(self.AverageRunTime)
			line += "," + str(self.ClocksPerSecond)
			line += "," + str(self.SeparationDistance)
			line += "," + str(self.CoveringRadius)
			line += "," + str(self.MeshSeparationRatio)

		line += "\n"
		return line

	

	def parseDataSetName(self):
		splitFilePath = self.InputFilePath.split("/")
		self.FileName = splitFilePath[-1]
		self.DataSetName = self.FileName.split(".")[0]
		splitFileName = self.DataSetName.split("-")

		if len(splitFileName) > 0:
			self.Method = splitFileName[0]

		if len(splitFileName) > 1:
			self.NumberIterations = splitFileName[1]

		if len(splitFileName) > 3:
			self.ExecutionNumber = splitFileName[3]

	# def DistributionName(self):
	# 	return self.DataSetName
