import config

config.outputFileName ="testFiles/2IIIFreq.log"
config.inputFileName = "testFiles/2IIIFreq.gjf"
import mod
mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc


# Get: route card, optimized coordinates, free energy
routeCard = IFProc.getRoute()[0]
optCoords = OFProc.getOptCoords()
freeE = OFProc.getFreeE()
constrainedG,constrainedH,constrainedTS = OFProc.getConstrainedThermochemistry(OFProc.getFreq())
normalTerm = OFProc.ifNormal()
atoms, ini = IFProc.getAtomsAndInitialCoords()
s2, s2a = OFProc.getSpinAnnihilation()
zeroPt = OFProc.getZeroPtEnergy()
NImag = OFProc.getNoImagFreq()

coordList = [atoms[i] +'\t\t\t'+ optCoords[i]+'' for i in range(len(atoms))]

# stringify
routeCard = " ".join(str(x) for x in routeCard)
coordList = ''.join(str(x) for x in coordList)
zeroPt = str(zeroPt)
if freeE == -1:
    freeE = 'Frequency calculation not performed'
else:
    freeE = str(freeE)
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
    f.write('\nFree Energy (Ha): '+freeE)
    f.write('\nThermochemistry accounting for '+str(config.N_Freeze)+' constrained periphery atoms:')
    f.write('\n\tFree Energy (Ha): '+str(constrainedG))
    f.write('\n\tEnthalpy (Ha): '+str(constrainedH))
    f.write('\n\tT*Entropy (Ha): '+str(constrainedTS))
    f.write('\n\nNumber of imaginary frequencies: '+str(NImag))
    if NImag >=1:
        f.write('\nWARNING 1+ IMAGINARY FREQUENCIES. Ignore this if this is a TS and there is only one.\nOtherwise, check if modes are in constraint space, or follow the imaginary modes\n'
                'If modes are not in constrainet space, thermochemistry (and everything else) IS WRONG\n')
    f.write('\nSpin contamination:\n')
    f.write('   Before: '+s2+'\n')
    f.write('   After: '+s2a)
    f.write('\n-------------------------------------------------\n')


