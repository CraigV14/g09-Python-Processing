#RULES:
# opt needs to be the last entry in the 1st input file
import re
import config
import numpy as np


# Set N and outputFileName from config as module wide variables
N_Frozen = config.N_Freeze
N = config.N
outputFileName = config.outPutFileName

def getOptCoords():
	# Searches the output file (outputFileName) and extracts the x,y,z positions of the optimized coordinates

	#Search string to find location of optimized coordinates
	lookup = " Number     Number       Type             X           Y           Z"
	nums = []
	#Open file, search for lookup, get line number
	with open(outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
		#Increment one more to get indexing right
		location += 1
		# Jump to location of
		f.seek(0)
		#Read in coords
		coords = f.readlines()[location:location+N]
	# Extract all numbers
	nums = [re.findall(r"[-+]?\d*\.\d+|\d+",x) for x in coords]
	#Parse just the (x,y,z) positions
	parsedCoords = [nums[i][3]+" "+nums[i][4]+" "+nums[i][5]+"\n" for i in range(N)]
	return parsedCoords

def getFreeE():
	# Returns the free energy after a frequency calculation
	lookup = ' Sum of electronic and thermal Free Energies='
	with open(outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
		f.seek(0)
		Elist = f.readlines()[location-1]

	freeE = re.findall(r"[-+]?\d*\.\d+|\d+", Elist)
	freeE = float(freeE[0])
	return freeE

# Future functions to add

import re
import numpy as np


def getHessian(outPutFileName, Numcoordinates, type):
    f = open(outPutFileName, "r")

    hessian_data = []
    for line in f:
        if "Force constants in " + type + " coordinates:" in line:
            for line in f:
                if "Leave Link" in line:
                    break
                line1 = line.replace("D", "E")
                hessian_data.append(line1.split())

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


def removeFixedRotAndTrans_q():
	# Removes the energy contributions from the rotational and translational q's of the fixed atoms
	appendedFreeE = 1
	return appendedFreeE

def getNoImagFreq():
	noImFreq = 0
	if noImFreq > 1 or noImFreq == 0:
		print 'WARNING, INCORRECT NUMBER OF IMAGINARY FREQUENCIES'
	return noImFreq