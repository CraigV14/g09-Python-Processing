import config
import mod
import cmath
import numpy as np
import re
config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/IIIFreqplus1.log"
config.inputFileName = 'C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/IIIFreqplus1.gjf'
temp = '373.15'

mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc
print config.N
print config.N_Freeze
# Read in hessian matrix in LT form
with open("C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/IIIplus1Derivs.7") as f:
    elements = f.readlines()
# Strip \n
elements = map(str.strip, elements)
# Split up each row into list
elements = map(lambda x: x.split(), elements)
# Flatten list of list
elements  = [y for x in elements for y in x]
# Replace D with e
elements = [w.replace('D', 'e') for w in elements]
# Cast as floats
elements = [float(w) for w in elements]
# Remove first 3N elements, these are not part of the Hessian
del elements[0:3*config.N]
# Size of LT matrix based on number of elements
arrSize =  int(-0.5 + (np.sqrt(1 + 8 * len(elements)) / 2))

# List -> LT matrix
indices = np.tril_indices(arrSize)
H = np.zeros((arrSize, arrSize))
H[indices] = elements

# Matrix is symmetric so fill it out
H = H + np.transpose(H) - np.diag(np.diag(H))
print H[0:3*(config.N-config.N_Freeze),0:3*(config.N-config.N_Freeze)]


# Conversion factor from Ha/bohr**2 to amu/s**2
convFactor = 4.3597439e-18/(0.5291772086e-10)**2/1.66053878e-27
# Mass weight matrix
H = H*convFactor
# Get masses in amu
masses = OFProc.getMasses()
# Vector of N masses to 3N masses
masses = [x for pair in zip(masses,masses,masses) for x in pair]

MminusHalf = np.diag(np.power(masses,-0.5))
# print MminusHalf
H = np.dot(np.dot(MminusHalf,H),MminusHalf)

# Get the eigenvalues
evals = np.linalg.eigvals(H)
evals = [complex(w) for w in evals]
# convert to wavenumbers
freq = [np.sqrt(w/(4.*3.14159**2*(2.99792458e10)**2)) for w in evals]

print freq
# Count number of imaginary frequencies
boolarr = np.array(np.iscomplex(freq),dtype=np.bool)
print "There are now "+str(np.sum(boolarr))+ " imaginary frequencies, but some might be small"
