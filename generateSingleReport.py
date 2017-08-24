import config
import numpy as np
np.set_printoptions(precision=6)
config.outputFileName ="testFiles/C2H4opt.log"
config.inputFileName = "testFiles/C2H4opt.gjf"
import mod
mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc
import thermoChem


# Get all the info from the output file
routeCard = IFProc.getRoute()[0]
optCoords = OFProc.getOptCoords()
# Check if constrained or unconstrained calc was performed
if config.N_Freeze == 0:
    freeE = OFProc.getFreeE()
else:
    constraintFreq, chemRotTrans, chemVibs, newNImag = thermoChem.getConstrainedFreq()
    constrainedG,constrainedH,constrainedTS,imagIgnored = thermoChem.getConstrainedThermochemistry(chemVibs)
normalTerm = OFProc.ifNormal()
atoms, ini = IFProc.getAtomsAndInitialCoords()
s2, s2a = OFProc.getSpinAnnihilation()
zeroPt = OFProc.getZeroPtEnergy()
NImag = OFProc.getNoImagFreq()

# Generate coordinate list in pretty format
coordList = []
optCoords = np.array(["%.6f" % w for w in optCoords.reshape(optCoords.size)])
optCoords = optCoords.reshape((config.N,3))

blank = '          '
for x in range(config.N):
    # Make slice points so spacing is always equal
    slice0 = 2-len(atoms[x])
    slice1 = 9-len(optCoords[x][0])
    slice2 = 12-len(optCoords[x][1])
    slice3 = 12-len(optCoords[x][2])
    coordList.append(atoms[x] +blank[0:slice0] +"      "+blank[0:slice1]+ optCoords[x][0]+blank[0:slice2]+optCoords[x][1]+blank[0:slice3]+optCoords[x][2]+'\n')

# stringify
if config.N_Freeze != 0:
    constraintFreq = " ".join(str('%.6f' %x) for x in constraintFreq)
    chemRotTrans = " ".join(str('%.6f' %x) for x in chemRotTrans)
    chemVibs = " ".join(str('%.3f' %x) for x in chemVibs)
routeCard = " ".join(str(x) for x in routeCard)
coordList = ''.join(str(x) for x in coordList)
zeroPt = str(zeroPt)
if config.N_Freeze == 0:
    if freeE == -1:
        freeE = 'Frequency calculation not performed'
    else:
        freeE = str(freeE)

if s2 == -1:
    s2 = 'None'
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
    if config.N_Freeze == 0:
        f.write('\nFree Energy (Ha): '+freeE)

    f.write('\n\nNumber of imaginary frequencies: '+str(NImag))
    if NImag >=1:
        f.write('\nWARNING 1+ IMAGINARY FREQUENCIES. Ignore this if this is a TS and there is only one.\nOtherwise, check if modes are in constraint space, or follow the imaginary modes\n'
                'If modes are not in constrainet space, thermochemistry (and everything else) IS WRONG\n')
    f.write('\nSpin contamination:\n')
    f.write('   Before: '+s2+'\n')
    f.write('   After: '+s2a)
    if config.N_Freeze != 0:
        f.write('\n\nThermochemistry accounting for ' + str(config.N_Freeze) + ' constrained periphery atoms:')
        f.write('\n\tNEW Number of imaginary freq, ignorng effects of peripheral atoms: '+str(newNImag))
        f.write('\n\n\tFree Energy (Ha): ' + str(constrainedG))
        f.write('\n\tEnthalpy (Ha): ' + str(constrainedH))
        f.write('\n\tT*Entropy (Ha): ' + str(constrainedTS))

        f.write('\n\n\tThe frequencies associated with the constrained peripheral atoms are (cm**-1):')
        f.write('\n\t'+constraintFreq)

        f.write('\n\n\tRotation and Translation Freq of the system (should be < +/-50 cm**-1):')
        f.write("\n\t"+chemRotTrans)

        f.write('\n\n\tVibration freqs used in calculating G (cm**-1):')
        f.write("\n\t"+chemVibs)
    f.write('\n-------------------------------------------------\n')


