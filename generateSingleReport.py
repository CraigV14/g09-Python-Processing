import config

config.outputFileName = 'testFiles/SiF3Oopt.log'
config.inputFileName = 'testFiles/SiF3Oopt.gjf'

import IFProc
import OFProc
# Get: route card, optimized coordinates, free energy
routeCard = IFProc.getRoute()
optCoords = OFProc.getOptCoords()
freeE = OFProc.getFreeE()
normalTerm = OFProc.ifNormal()
atoms, ini = IFProc.getAtomsAndInitialCoords()


coordList = [atoms[i] +'    '+ optCoords[i] for i in range(len(atoms))]

# stringify
routeCard = " ".join(str(x) for x in routeCard)
coordList = ''.join(str(x) for x in coordList)
if freeE == -1:
    freeE = 'Frequency calculation not performed'
else:
    freeE = str(freeE)+' kJ/mol'

# Create report
with open('report.txt', 'w') as f:
    f.write('Job details for: '+config.outputFileName+ '\n\n')
    f.write('Normal termination? '+str(normalTerm)+'\n\n')
    f.write('Route Card: '+routeCard+'\n')
    f.write('Optimized coordinates:\n'+coordList)
    f.write('\nFree Energy: '+freeE)
    f.write('\n-------------------------------------------------\n')
