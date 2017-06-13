import config
import mod

config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.log"
config.inputFileName = 'C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/SiVinylFrozenOpt2.gjf'

config.N = mod.setN()
config.N_Frozen = mod.setN_Freeze()
# print config.N
# print config.N_Freeze

import OFProc

print OFProc.getOptCoords()
