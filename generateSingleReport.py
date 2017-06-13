import config

config.outputFileName ="C:/Users/Craig/Box Sync/UCSB2/Research/HomolysisPaper/butylBridge[5V-5II]/3/BB3.log"
config.inputFileName = "C:/Users/Craig/Box Sync/UCSB2/Research/HomolysisPaper/butylBridge[5V-5II]/3/BB3.log"

import IFProc
import OFProc
# Get: route card, optimized coordinates, free energy
routeCard = IFProc.getRoute()
optCoords = OFProc.getOptCoords()
freeE = OFProc.getFreeE()
normalTerm = OFProc.ifNormal()
atoms, ini = IFProc.getAtomsAndInitialCoords()
s2, s2a = OFProc.getSpinAnnihilation()
zeroPt = OFProc.getZeroPtEnergy()

coordList = [atoms[i] +'  '+ optCoords[i]+'    ' for i in range(len(atoms))]

# stringify
routeCard = " ".join(str(x) for x in routeCard)
coordList = ''.join(str(x) for x in coordList)
zeroPt = str(zeroPt)
if freeE == -1:
    freeE = 'Frequency calculation not performed'
else:
    freeE = str(freeE)+' kJ/mol'
if s2 == -1:
    s2 = 'No unpaired electrons'
    s2a = s2
else:
    s2a = str(s2a)
    s2 = str(s2)
# Create report
with open('report.txt', 'w') as f:
    f.write('Job details for: '+config.outputFileName+ '\n\n')
    f.write('Normal termination? '+str(normalTerm)+'\n\n')
    f.write('Route Card: '+routeCard+'\n')
    f.write('Optimized coordinates:\n'+coordList)
    f.write('\nZero Point Energy (Hartrees): '+zeroPt)
    f.write('\nFree Energy: '+freeE)
    f.write('\nSpin contamination:\n')
    f.write('   Before: '+s2+'\n')
    f.write('   After: '+s2a)
    f.write('\n-------------------------------------------------\n')


