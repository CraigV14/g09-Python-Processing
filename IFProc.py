import re

def getAtomsAndTitleCard(N, inputFileName):
	# Reads the input file to:
	# 	1. Get the title card
	# 	2. Find the location of the title card
	# 	3. Get the list of atoms
	#	4. Get the list of fixed and not fixed atoms
	lookup = "#"
	with open(inputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
	location-=1
	with open(inputFileName) as f:
		titleCard = f.readlines()[location]
		f.seek(0)
		inputList = f.readlines()[location+5:location+5+N]
	# Split all entries into list elements based on whitespace
	inputList = [i.split() for i in inputList]
	atomList = [inputList[i][0] for i in range(N)]

	# Check if any of the atoms are actually frozen.
	# Otherwise set all elements of freezeList = 0 (i.e. all atoms can move)
	try:
		holdings = [int(inputList[i][1]) for i in range(N)]
	except ValueError:
		holdings = [0 for i in range(N)]


	return location+1, titleCard, atomList, holdings

def appendTitleCard(titleCard, T):
	# For frequency calcluations. Removes opt from the title card and replaces it with freq temp=T
	# Inputs:
	# 			titleCard: title card. Get from getAtomsAndTitleCard(N, inputFileName)
	# 			T: temperature to perform freq calc at. User input


	# find opt location
	slicePt = titleCard.find("opt")
	# Remove opt...
	titleCard = titleCard[:slicePt]
	# Add freq and temp
	titleCard = titleCard+"freq temp=" + str(T)+"\n"
	return titleCard