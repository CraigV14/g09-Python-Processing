# RULES:
# only freeze atoms through internal coordinates
import linecache
import re

import numpy as np

import config

# Get outputfile name, N, and N_Freeze from config.py
outputFileName = config.outputFileName
N = config.N
N_Freeze = config.N_Freeze

## OPTIMIZATION RELATED FUNCTIONS ##
def getOptCoords():
	# Searches the output file (outputFileName) and extracts the x,y,z positions of the optimized coordinates as a space
	# separated list of strings

	#Search string to find location of optimized coordinates
	lookup = " Number     Number       Type             X           Y           Z"
	#Open file, search for lookup, get line number
	location = findLocation(lookup,False) + 1
	with open(outputFileName) as f:
		coords = f.readlines()[location:location+N]
	# Extract all numbers
	nums = [re.findall(r"[-+]?\d*\.\d+|\d+",x) for x in coords]
	#Parse just the (x,y,z) positions
	parsedCoords = [nums[i][3]+" "+nums[i][4]+" "+nums[i][5]+"\n" for i in range(N)]
	return parsedCoords

def getZeroPtEnergy():
	location = -1
	lookup = ' SCF Done:'
	with open(outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line[0:10]:
				location = num
		f.seek(0)
		readLine = f.readlines()[location-1]
	readLine = readLine.split()
	zeroPtEnergy = float(readLine[4])
	return zeroPtEnergy

def getModRedundantCoords():
	# Read in all the modredundant coordinates as a list of string.
	# A value of -1 means no modredundant coordinates have been detected
	lookup = ' The following ModRedundant input section has been read:'
	location = findLocation(lookup,True)
	with open(outputFileName) as f:
		if location != -1:
			i = 0
			MRCoords = []
			# read in modredundant coords until theres no more (entry is NAtoms=)
			while True:
				f.seek(0)
				readLine = f.readlines()[location+i]
				MRCoords.append(readLine.split())
				# Criteria to exit (100000 iterations force exits, which means something went wrong)
				if MRCoords[i][0] == 'NAtoms=' or i > 100000:
					# 'NAtoms=' is the 2nd line that follows the last modredundant entry. The 1st line is an empty space
					# so delete it
					del MRCoords[-1]
					break
				i += 1
		else:
			MRCoords = -1
	return MRCoords

def getHessian(Numcoordinates, type):
	# returns hessian as a numpy array
	# type = "internal" or "Cartesian"
	f = open(outputFileName, "r")
	hessian_data = []
	for line in f:
		if "Force constants in " + type + " coordinates:" in line:
			for line in f:
				if "Leave Link" in line:
					break
				line1 = line.replace("D", "E")
				hessian_data.append(line1.split())
	f.close()
	n = Numcoordinates
	o = 5  # number of columns that gaussian prints ( current version = 5) , not checked for smaller number of coordinates (rare)
	# variables used to parse through data
	m = 0
	p = n / o + 1
	temp = 0
	q = 0

	hessian = np.zeros(shape=(n, n))

	for i in range(0, n):
		p = i / o
		if p < 2:
			q = 0
		else:
			q = p - 1
		if m % o == 0:
			temp = temp + q * o
		for j in range(m, n):
			hessian[j][m] = float(hessian_data[(n) * p - temp + p + j + 1 - p * o][m + 1 - o * p])
			hessian[m][j] = hessian[j][m]
		m = m + 1

	return hessian

def getSpinAnnihilation():
	lookup = ' Annihilation of the first spin contaminant:'
	location = findLocation(lookup,False)
	if location != -1:
		with open(outputFileName) as f:
			f.seek(0)
			readLine = f.readlines()[location]
		readLine = readLine.split()
		s2 = float(readLine[3][0:-1])
		s2a = float(readLine[5])
	else:
		s2 = -1
		s2a = -1
	return s2,s2a

## FREQUENCY RELATED FUNCTIONS ##
def temperature():
# returns temperature from output frequency file
	lookup = 'emperature'
	line_num = -1
	with open(outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				line_num = num
				break
	if line_num == -1:
		temperature = -1
	else:
		line = linecache.getline(outputFileName, line_num)
		# assuming temperature is the last input, splits the line at "emperature=" and returns value after "="
		temperature = (line.split("emperature=", 1)[1]).strip('\n')
	return float(temperature)

def getFreeE():
	# Returns the free energy after a frequency calculation
	# A value of -1 means the free energy was not found (no freq calc)
	lookup = ' Sum of electronic and thermal Free Energies='
	location = findLocation(lookup,False)
	with open(outputFileName) as f:
		Elist = f.readlines()[location-1]

	# Check if free energy exists (i.e. there was an actual freq calculation)
	if location != -1:
		freeE = re.findall(r"[-+]?\d*\.\d+|\d+", Elist)
		freeE = float(freeE[0])
	else:
		freeE = -1
	return freeE

def partition(type):
	# returns the natural log of different components of the partition function
	# type = 1 returns total (bot)
	# type = 2 returns electronic
	# type = 3 returns translational
	# type = 4 returns rotational
	# type = 5 returns vibrational

	index = 0
	line_plus = 0
	split_line = []

	if type == 1:
		lookup = 'Total Bot'
		index = 1
	if type == 2:
		lookup = 'Electronic'
	if type == 3:
		lookup = 'Translational'
	if type == 4:
		lookup = 'Rotational'
	if type == 5:
		lookup = 'Total Bot'
		index = 1
		line_plus = 2

	with open(outputFileName) as myFile:
		for num, line in enumerate(myFile, 1):
			if lookup in line:
				line_num = num + line_plus

	line = linecache.getline(outputFileName, line_num)
	split_line.append(line.split())
	LnQ = split_line[0][3 + index]
	return float(LnQ)

def nearzerovib(N_fix):
	# returns the sum of the natural log of the 3*number of fixed coordinate partition functions
	split_line = []
	LnQ_nearzero = float(0)

	with open(outputFileName) as myFile:
		for num, line in enumerate(myFile, 1):
			if "Total Bot" in line:
				line_num = num + 3

	for i in range(0, 3 * N_fix):
		line = linecache.getline(outputFileName, line_num + i)
		split_line.append(line.split())
		LnQ_nearzero = LnQ_nearzero + float(split_line[i][5])

	return LnQ_nearzero

def removeFixedRotAndTrans_q():
	# Removes the energy contributions from the rotational and translational q's of the fixed atoms
	appendedFreeE = 1
	return appendedFreeE

def getNoImagFreq():
	with open(outputFileName) as f:
		# Read in the whole file b/c there's no great way otherwise
		line = f.read()

	location = line.find('\NImag')
	if location == -1:
		noImFreq = -1
	else:
		noImFreq = int(line[location+7])
	# Clear line since it reads in the whole damn file
	del line
	return noImFreq

def setNoFrozen():
	N_Freeze = 0
	#	See if theres any MR coordinates
	MR = getModRedundantCoords()
	if MR != -1:
		for i in range(len(MR)):
			if MR[i][0] == 'X':
				if MR[i][3] == 'F':
					N_Freeze += 1
	# # Now see if theres any frozen cartesian coordinates if theres no MR coords
	# else:
	# 	N_Freeze = IFProc.getFrozenCartNo()
	return N_Freeze

## EITHER OPT OR FREQ ##
def ifNormal():
# returns 1 if the log file has terminated normally, otherwise returns 0
	split_line = []
	number_lines = sum(1 for line in open(outputFileName))
	line = linecache.getline(outputFileName, number_lines)
	split_line.append(line.split())
	if(split_line[0][0]=="Normal"):
		normal = True
	else:
		normal = False
	return normal

def findLocation(lookup,firstInstance):
	# Returns the 0 indexed location for a line in the output file
	# Inputs:
	# 			lookup: string. phrase to search for
	# 			firstInstance: boolean. If true: find location of the first instance
	# 									If false: find location of last instance
	# Location of -1 means phrase is not found
	location = -1
	with open(outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				if firstInstance is True:
					break
	return location

