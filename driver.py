import config
import mod

config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.log"
config.inputFileName = 'C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.gjf'

mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc
temp = '373.15'
# Fetch only the first row, which is the atom list, we don't care about the initial coordinates
atomList = IFProc.getAtomsAndInitialCoords()[0]
# Get modredundant coordinates
modRed = OFProc.getModRedundantCoords()

# Parse only the frozen coordinates
frozenAtomList = []
for i in range(len(modRed)):
    if modRed[i][3] == 'F':
        frozenAtomList.extend(modRed[i][1])
        frozenAtomList.extend(modRed[i][2])
# Remove duplicates
frozenAtomList= list(set(frozenAtomList))
# Removes '*' if its there. Does nothing if its not
try:
    frozenAtomList.remove('*')
except ValueError:
    pass
# Make the frozen atoms super duper heavy
for i in range(config.N_Freeze):
    atomList[int(frozenAtomList[i])-1] += "(Iso=10000000)"
# Get the optimized coordinates
optCoords = OFProc.getOptCoords()
# Generate the list of now frozen coordinates to do the frequency calculation on
freqCoordList = [atomList[x]+'\t'+optCoords[x] for x in range(config.N)]

# Append the title card
route = IFProc.getRoute()
# Strip \n from last term
route[-1] = route[-1][0:-1]
# Get rid of opt
sub = 'opt'
optString = [s for s in route if sub.lower() in s.lower()]
route.remove(optString[0])
# Add freq and punch derivatives
route.append('punch(derivatives)')
route.append('freq')
route.append('temp='+temp+'\n')


with open(config.inputFileName) as f:
    content = f.readlines()
# Find


print content
print modRed
print freqCoordList
