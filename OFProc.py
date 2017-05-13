#RULES:
# opt needs to be the last entry in the 1st input file
import re

def setN(outPutFileName):
	#Search the output file for the number of atoms used

	#String to find
	lookup =" NAtoms"
	with open(outPutFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		f.seek(0)
		Nlist = f.readlines()[location-1]
	nums = re.findall(r'\d+', Nlist)
	N = int(nums[0])
	return N

def getOptCoords(N, outputFileName):
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

def concatOptCoordsWithAtoms(atoms, freezeList, optCoords,N):
	# make the list for a frequency calculation
	# mashes together the list of atoms, coordinates, and handles the case where atoms are frozen
	#
	freqInput=[]
	for i in range(N):
		if freezeList[i] == -1:
			atoms[i] = atoms[i][0:2]+"(Iso=100000000000)          "
		else:
			atoms[i] = atoms[i][0:3]
		freqInput.append(atoms[i]+"          "+optCoords[i])
	return freqInput

def getFreeE(outputFileName):
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


