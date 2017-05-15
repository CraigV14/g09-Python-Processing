import re
import config

# Set N and inputFileName from config
N = config.N
inputFileName = config.inputFileName

def getTitleCard():
	lookup = "#"
	with open(inputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		location-=1
		f.seek(0)
		titleCard = f.readlines()[location]
	return titleCard

def getAtomsAndInitialCoords():
	lookup = "#"
	with open(inputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		location-=1
		f.seek(0)
		inputList = f.readlines()[location+5:location+5+N]
		inputList = [i.split() for i in inputList]
		print inputList[1][2]
		atomList = [inputList[i][0] for i in range(N)]
		iniCoords = [inputList[i][1] for i in range(N)]

	return atomList, iniCoords

def getRedundantCoords():
	rCoords = 1
	return rCoords

print getAtomsAndInitialCoords()