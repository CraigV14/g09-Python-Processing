import config
import mod

config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.log"
config.inputFileName = 'C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.gjf'

mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc

# Fetch only the first row, which is the atom list, we don't care about the coordinates
atomList = IFProc.getAtomsAndInitialCoords()[0]
modRed = OFProc.getModRedundantCoords()
frozenAtomList = []
j = 0

print modRed

print zip(*modRed)[3]

# Parse only the frozen coordinates
for i in range(len(modRed)):
    if modRed[i][3] == 'F':
        frozenAtomList.extend(modRed[i][1])
        frozenAtomList.extend(modRed[i][2])

print frozenAtomList
# Remove duplicates
frozenAtomList= list(set(frozenAtomList))


print frozenAtomList
#
# for i in range(config.N_Freeze):
#     atomList[int(frozenAtomList[i])-1] += "(Iso=1000000)"
#


