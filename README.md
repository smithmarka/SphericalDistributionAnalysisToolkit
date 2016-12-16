Spherical Distribution Analysis Kit
======

Spherical Distribution Analysis Kit (SDAK) is a console based application built to assist with the analysis of Spherical Point distributions. The kit takes input in the form of a CSV file with X, Y, Z coordinates and calculates a number of metrics to determine the uniformity of the distribution of the input points.

The original kit was mostly written using as few dependency libraries, but since some of the metrics required the usage of the scipy and numpy packages the kit has been completely rewritten to utilize these libraries more heavily and offer a more robust and tested experience.

Metrics
-------------
* Separation Distance (Larger Result = More Even Distribution)
	
The minimum distance between any two points in the distribution represents the Separation Distance. The greater the value the more even the distribution. To calculate this value the kit uses a simple double loop through each of the points in the distribution, computing the haversine distance between every combination of points except distance(pointX, pointX). The minimum distance found in this double loop becomes the Separation Distance for the distribution. For larger point distributions this might become an unrealistic approach, and since we already compute the Voronoi diagram below a future update may replace this algorithm.

* Covering Radius (Mesh Norm) (Smaller Result = More Even Distribution)

The Covering Radius measures the minimum of the maximum distance between any neighbouring points, also referred to as the Mesh Norm. To calculate this value the kit uses the scipy.spatial library to generate a object used to represent the Voronoi diagram. The kit looks at each vertice and determines which Voronoi regions it belongs to. The for each of these regions it calculates the haversine distance between the vertice and the point that was used to generate the Voronoi region. The local minimum is determined for each region, and from this a global maximum is determine which is used as the Covering Radius.

* Mesh-Separation Ratio (Smaller Result = More Even Distribution)

The Mesh-Separation Ratio is closely related to both the Covering Radius and the Separation Distance, calculated by dividing the Covering Radius by the Separation Distance. The smaller the result the more even the distribution. 



Prerequisites
-------------
* Python 3.4
* Python 3.4 venv
* scipy >= 0.18 (As of writing the version of scipy stored in the pip repository does not meet the minimum requirements and will need to be built from source)
* numpy
* cython
* pandas
* Build from source prerequisites (Only required to build Scipy)
	gfortran
	libatlas-dev 
	liblapack-dev 
* matplotlib OS prequisites
	libgtk2.0-dev 
	python3-tk 
	tk-dev

Installation
-------------
* Kit was built and tested on standard Debian Jessie but should run on any system that can execute Python code
* OS Prerequisite Installation: A script named setup1.sh has been provided to assist the installation of OS specific packages required to build and run the kit. The script works on the official build system but is not particularly robust so it is recommended that you review the script and perhaps manually install the necessary packages.

* Virtual Environment / SDAK Build: A script named setup2.sh has been provided to assist with this step, again it works on the official build system to cleanly install from a fresh copy of source by users are encouraged to review and handle as necessary.


Running Spherical Distribution Analysis Kit
------
source ./bin/activate
python sphericalDistributionAnalysisKit.py inputFolderPath [--MetricsOutput=MetricsOutputFolder] [--GenerateWaveFront=WaveFrontFolder]

This program was built in a pyvenv virtual environment. Unless you have all the proper python libraries installed on your machine you should run it within the context of the virtual environment by executing the first line before the second.

The program will recursively search each folder in the inputFolderPath loading the data from each CSV file of X, Y, Z coordinates found. The values of each metric described above will be calculated by the program and outputted to MetricsOutputFolder/Results.csv. If a '-runtime' file is located in the same directory as the input file then the runtimes will be added to the metrics output. If the optional WaveFrontFolder is set then a Wavefront file will be generated for every distribution processed by the kit. Note that if you select this option and you have a large number of distributions you will quickly fill up your drive with what is essentially a copy of the original data.

The wavefront files can be used to generate visualizations using blender (you will have to install blender) with the following command:
	- blender render.blend --background --python generateBlenderVisualizations.py --InputFolderPath=../Wavefront/ --OutputFolderPath=../Visualizations/

To generate the final results you can use the command:
	source ./bin/activate
	python generateGraphs.py ../Results/

This will output a number of png files of the graphs and a number of CSV files with the data used to generate those graphs.



Acknowledgments
------
A thank you goes out to these projects for making the implementation of this kit possible

+ [![DOI](https://zenodo.org/badge/6247/tylerjereddy/py_sphere_Voronoi.svg)](http://dx.doi.org/10.5281/zenodo.13688)

Author
------
**Mark Smith**

+ smithmarka@gmail.com


