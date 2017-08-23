import config
import mod

import numpy as np
# config.outputFileName = "testFiles/projectionTest/salman.log"
# config.inputFileName = "testFiles/projectionTest/salman.gjf"

config.outputFileName = "testFiles/projectionTest/TiGraftWumboFine.log"
config.inputFileName = "testFiles/projectionTest/TiGraftWumboFine.gjf"

temp = '373.15'
np.set_printoptions(suppress=True)
mod.setN()
mod.setN_Freeze()
unfrozen = config.N-config.N_Freeze
import IFProc
import OFProc
import thermoChem
# Read in hessian matrix in LT form
# with open("testFiles/projectionTest/salman.7") as f:
#     elements = f.readlines()

H = thermoChem.getHessian("TiGraftWumboFine")

# Take minor of the Hessian, only leaving entries from the non-peripheral atoms
H = H[0:3*unfrozen,0:3*unfrozen]

# Reconstruct full Hessian. Set diagonal block of peripheral atoms to 10^-8 to avoid spurious imaginary freqs.
# Set off diagonal blocks to 0. Epsilon is a temporary matrix
epsilon = np.diag(10.**(-8)*np.ones(3*config.N))

# Insert Hessian minor of chemical system in.
epsilon[:3*unfrozen,:3*unfrozen] = H
# Rename and delete epsilon
H = epsilon
del epsilon

# Conversion factor from Ha/bohr**2 to amu/s**2
convFactor = 4.3597439e-18/(0.5291772086e-10)**2/1.66053878e-27
H = H*convFactor
# Get masses in amu
masses = OFProc.getMasses()

# Vector of N masses to 3N masses
masses = [x for pair in zip(masses,masses,masses) for x in pair]
MminusHalf = np.diag(np.power(masses,-0.5))

# Mass weight matrix
H = np.dot(np.dot(MminusHalf,H),MminusHalf)
# Get the eigenvalues
evals = np.linalg.eigvals(H)

# convert to wavenumbers
allFreq = [np.sign(w)*np.sqrt(np.abs(w)/(4.*3.14159**2*(2.99792458e10)**2)) for w in evals]
signList = np.sign(allFreq)
# Sort by magnitude so the smallest freq's get put to the bottom regardless of size
# However, the permutations done by sorting also need to be carried over to the list of signs to preserve which are
# imaginary
sortedFreq,allSign = zip(*sorted(zip(np.abs(allFreq),signList)))
allFreq = np.multiply(sortedFreq,allSign)

# Sort the frequencies into 3 contributions
# constraintFreq: frequencies of the constrained peripheral atoms that will be pruned
# chemFreq: frequencies of the system excluding peripheral atoms(where the chemistry happens)
# chemRotTrans: the lowest 6 frequencies that correspond to rotations and vibrations
# chemVib: 3n-6 vibrational modes, where n is # of non constrained atoms

constraintFreq = allFreq[:3*config.N_Freeze]
chemFreq = allFreq[3*config.N_Freeze:]
chemRotTrans = chemFreq[:6]
chemVibs = chemFreq[6:]

# Lastly, count number of imaginary frequencies
newNImag = 0
for x in allSign:
    if x == -1:
        newNImag+=1



constrainedG, constrainedH, constrainedTS, ImagFreqIgnored = np.real(OFProc.getConstrainedThermochemistry(allFreq))
#
# with open('ThermochemPeripheralsProjectedOut.txt', 'w') as f:
#     f.write("Thermochemistry data for "+config.outputFileName+" after projecting out "+str(config.N_Freeze)+" peripheral atoms\n")
#     f.write("There are now "+str(newNImag)+ " imaginary frequencies\n")
#     if newNImag == 0 or 1:
#         f.write("Free Energy (Ha): "+str(constrainedG)+'\n')
#         f.write("Enthalpy (Ha): " + str(constrainedH)+'\n')
#         f.write("T*S (Ha): " + str(constrainedTS)+'\n')

