import re
import config
import OFProc
# Set N and inputFileName from config
# N = config.setN()
inputFileName = config.inputFileName

def getRoute():
	# Returns the title card as a list where each element is an option
	lookup = "#"
	with open(inputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		location-=1
		f.seek(0)
		titleCard = f.readlines()[location]
		titleCard = titleCard.split(' ')
	return titleCard

def getAtomsAndInitialCoords():
	# Returns the list of atoms and initial coordinates
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
		atomList = [inputList[i][0] for i in range(N)]
		iniCoords = [inputList[i][-3]+' '+inputList[i][-2]+' '+inputList[i][-1] for i in range(N)]

	return atomList, iniCoords

def getFrozenCartNo():
	noFrozenCart = 0
	lookup = '#'
	location = OFProc.findLocation(lookup,True)
	with open(inputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		f.seek(0)
		list = f.readlines()[location+4:location+4+N]
		list = [i.split() for i in list]
	for i in range(N):
		try:
			int(list[i][1])
			if int(list[i][1]) == -1:
				noFrozenCart+=1
		except ValueError:
			noFrozenCart+=0
	return noFrozenCart