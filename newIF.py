import config

N = config.N
inputFileName = config.inputFileName

def makeFreqInputFile(freqInput, titleCard,tCardLocation):
	# copy all settings from opt input file
	with open(inputFileName) as f:
		inputFile = f.readlines()
	# print(inputFile)
	tCardLocation-=1
	inputFile[tCardLocation] = titleCard
	inputFile[tCardLocation+5:tCardLocation+5+N] = freqInput


	with open('freqInput.gjf', 'w') as f:
		for i in range(len(inputFile)):
			f.write(inputFile[i])

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

def concatOptCoordsWithAtoms(atoms, freezeList, optCoords,):
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
