import config
import mod
import numpy as np

# config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/IIIminus1.log"
# config.inputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/IIIminus1.gjf"

# config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.log"
# config.inputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.gjf"

config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/3IV-5III.log"
config.inputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/3IV-5III.gjf"

# System inputs 3 and 4, temperature and option to punch derivatives1
temp = '373.15'
punch = False


mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc

# Fetch only the first row, which is the atom list, we don't care about the initial coordinates
atomList = IFProc.getAtomsAndInitialCoords()[0]
# Get modredundant coordinates
modRed = OFProc.getModRedundantCoords()

# Get the list of frozen atoms
frozenAtomList = OFProc.getNoFrozenAndFrozenList()[1]

for i in range(config.N_Freeze):
    index = int(frozenAtomList[i])-1
    atomList[index] += "(Iso=100000000)"

# Get the optimized coordinated
optCoords = OFProc.getOptCoords()

optCoords = np.array(["%.6f" % w for w in optCoords.reshape(optCoords.size)])
optCoords = optCoords.reshape((config.N,3))
# Generate the list of new frozen, optimized coordinates to do the frequency calculation on
freqCoordList = []
blank = '          '
for x in range(config.N):
    # Make slice points so spacing is always equal
    slice0 = 2-len(atomList[x])
    slice1 = 9-len(optCoords[x][0])
    slice2 = 12-len(optCoords[x][1])
    slice3 = 12-len(optCoords[x][2])
    freqCoordList.append(atomList[x] +blank[0:slice0] +"      "+blank[0:slice1]+ optCoords[x][0]+blank[0:slice2]+optCoords[x][1]+blank[0:slice3]+optCoords[x][2]+'\n')


#########################
# Append the title card #
#########################

route,tCardLoc = IFProc.getRoute()
# Strip \n from last term
route[-1] = route[-1][0:-1]
# Get rid of opt
sub = 'opt'
optString = [s for s in route if sub.lower() in s.lower()]
route.remove(optString[0])
# Add freq and punch derivatives
if punch == True:
    route.append('punch(derivatives)')
route.append('freq')
route.append('temp='+temp+'\n')

with open(config.inputFileName) as f:
    content = f.readlines()
# Find
content[tCardLoc] = ' '.join(route)
content[tCardLoc+5:tCardLoc+5+config.N] = freqCoordList

# Remove Modredundant Coord Section
del content[tCardLoc+6+config.N:tCardLoc+6+config.N+len(modRed)+1]

with open('FreqTest.txt', 'w') as f:
    [f.write(content[i]) for i in range(len(content))]

