
import os.path
import math
import numpy as np
import scipy.spatial


class SphericalDistribution:

	def __init__(self, filePath):
		self.InputFilePath = filePath
		self.points = None
		self.SeparationDistance = None
		self.PackingRadius = None
		self.CoveringRadius = None
		self.MeshSeparationRatio = None
		self.DataSetName = None

		self.loadData()
		self.determineDataSetName()

		self.Voronoi = None
		if self.points is not None:
			self.Voronoi = scipy.spatial.SphericalVoronoi(self.points)

		self.calculateSeparationDistance()
		self.calculatePackingRadius()
		self.calculateCoveringRadius()
		self.calculateMeshSeparationRatio()

	def loadData(self):
		self.points = np.genfromtxt(self.InputFilePath, delimiter=",")

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

	def vectorAngle(point1, point2):
		angle = 0

		if len(point1) is 3 or len(point2) is 3:
			distance = SphericalDistribution.haversineDistance(point1, point2)

			try:
				angle = (2 * math.asin(distance / 2))
			except:
				# angle = 3.1415926535897932384
				angle = math.pi
		return angle

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

	def loadInputData(self):

		inputFile = open(self.InputFilePath, 'r')
		pointId = 0
		inputArray = []
		pointArray = []

		for line in inputFile:
			splitLine = line.split(',')
			x = 0
			y = 0
			z = 0

			if len(splitLine) is not 3:
				splitLine = line.strip(' \t\n\r').split('  ')

			if len(splitLine) is not 3:
				raise ValueError("Fuck it you entered wrong data at line: ")

			x = float(splitLine[0])
			y = float(splitLine[1])
			z = float(splitLine[2])

			pointArray.append(Point(pointId, x, y, z))
			inputArray.append([splitLine[0], splitLine[1], splitLine[2]])

			pointId = pointId + 1

		self.PointArray = pointArray
		self.InputArray = inputArray
		self.NDArray = self.generateNDArray()
		self.Voronoi = scipy.spatial.SphericalVoronoi(self.NDArray)

	def outputMetrics(self, headerFlag):
		line = None

		if headerFlag is True:
			line = "DataSetName,FileName,NumPoints,SeparationDistance,PackingRadius,"
			line = line + "MeshNorm-CoveringRadius,MeshRatio-MeshSeparationRatio"
		else:
			line = self.DataSetName + "," + self.InputFilePath + ","
			line = line + str(len(self.Voronoi.points)) + "," + str(self.SeparationDistance)
			line = line + "," + str(self.PackingRadius) + "," + str(self.CoveringRadius)
			line = line + "," + str(self.MeshSeparationRatio)

		return line

	def determineDataSetName(self):
		splitFilePath = [os.path.split(self.InputFilePath)[0].split("/")[-1], os.path.split(self.InputFilePath)[-1]]
		self.DataSetName = splitFilePath[0]

	def DistributionName(self):
		return self.DataSetName + "-" + str(len(self.Voronoi.points))