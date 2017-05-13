def makeFreqInputFile(inputFileName, freqInput, titleCard,tCardLocation,N):
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
