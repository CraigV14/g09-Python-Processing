#RULES:
# opt needs to be the last entry in the 1st input file
import re
import config

# Set N and outputFileName from config
N = config.N
outputFileName = config.outPutFileName

def getOptCoords():
	# Searches the output file (outputFileName) and extracts the x,y,z positions of the optimized coordinates
	# Inputs:
	# 			N: number of atoms
	# 			outputFileName: name of the output file

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
