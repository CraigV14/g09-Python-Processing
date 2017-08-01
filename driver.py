import config
import mod
import cmath
import numpy as np
import re
config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/freqSiF3OHopt.log"
config.inputFileName = 'C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/freqSiF3OHopt.gjf'

mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc

print OFProc.getConstrainedThermochemsitry()
