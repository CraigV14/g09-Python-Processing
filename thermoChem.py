import numpy as np
import config
# Get outputfile name, N, and N_Freeze from config.py
outputFileName = config.outputFileName
inputFileName = config.inputFileName

N = config.N
N_Freeze = config.N_Freeze
unfrozen = N-N_Freeze

import OFProc
import IFProc

def getHessian():
    # Returns the Cartesian Hessian (Ha/Bohr**2) as a numpy array, is read from fort.7
    with open(outputFileName[:-4]+".7") as f:
        elements = f.readlines()
    # Strip \n
    elements = map(str.strip, elements)
    # Split up each row into list
    elements = map(lambda x: x.split(), elements)
    # Flatten list of list
    elements = [y for x in elements for y in x]
    # Replace D with e
    elements = [w.replace('D', 'e') for w in elements]
    # Cast as floats
    elements = [float(w) for w in elements]
    # Remove first 3N elements, these are not part of the Hessian
    del elements[0:3 * config.N]
    # Size of LT matrix based on number of elements
    arrSize = int(-0.5 + (np.sqrt(1 + 8 * len(elements)) / 2))

    # List -> LT matrix
    indices = np.tril_indices(arrSize)
    H = np.zeros((arrSize, arrSize))
    H[indices] = elements

    # Matrix is symmetric so fill it out
    H = H + np.transpose(H) - np.diag(np.diag(H))
    return H

def getConstrainedFreq():
    H = getHessian()
    # Take minor of the Hessian, only leaving entries from the non-peripheral atoms
    H = H[0:3 * unfrozen, 0:3 * unfrozen]

    # Reconstruct full Hessian. Set diagonal block of peripheral atoms to 10^-8 to avoid spurious imaginary freqs.
    # Set off diagonal blocks to 0. Epsilon is a temporary matrix
    epsilon = np.diag(10. ** (-8) * np.ones(3 * config.N))

    # Insert Hessian minor of chemical system in.
    epsilon[:3 * unfrozen, :3 * unfrozen] = H
    # Rename and delete epsilon
    H = epsilon
    del epsilon
    # Conversion factor from Ha/bohr**2 to amu/s**2
    convFactor = 4.3597439e-18 / (0.5291772086e-10) ** 2 / 1.66053878e-27
    H = H * convFactor
    # Get masses in amu
    masses = OFProc.getMasses()

    # Vector of N masses to 3N masses
    masses = [x for pair in zip(masses, masses, masses) for x in pair]
    MminusHalf = np.diag(np.power(masses, -0.5))

    # Mass weight matrix
    H = np.dot(np.dot(MminusHalf, H), MminusHalf)
    # Get the eigenvalues
    evals = np.linalg.eigvals(H)

    # convert to wavenumbers
    allFreq = [np.sign(w) * np.sqrt(np.abs(w) / (4. * 3.14159 ** 2 * (2.99792458e10) ** 2)) for w in evals]
    signList = np.sign(allFreq)
    # Sort by magnitude so the smallest freq's get put to the bottom regardless of size
    # However, the permutations done by sorting also need to be carried over to the list of signs to preserve which are
    # imaginary
    sortedFreq, allSign = zip(*sorted(zip(np.abs(allFreq), signList)))
    allFreq = np.multiply(sortedFreq, allSign)

    # Sort the frequencies into 3 contributions
    # constraintFreq: frequencies of the constrained peripheral atoms that will be pruned
    # chemFreq: frequencies of the system excluding peripheral atoms(where the chemistry happens)
    # chemRotTrans: the lowest 6 frequencies that correspond to rotations and vibrations
    # chemVib: 3n-6 vibrational modes, where n is # of non constrained atoms
    constraintFreq = allFreq[:3 * config.N_Freeze]
    chemFreq = allFreq[3 * config.N_Freeze:]
    chemRotTrans = chemFreq[:6]
    chemVibs = chemFreq[6:]

    # Lastly, count number of imaginary frequencies
    newNImag = 0
    for x in allSign:
        if x == -1:
            newNImag += 1

    return constraintFreq, chemRotTrans, chemVibs, newNImag

def getConstrainedThermochemistry(vibFreqs):
    # freqList = getFreq()
    lenI = len(vibFreqs)
    # Remove imaginary (negative) frequencies
    freqList = [x for x in vibFreqs if x > 0]
    lenF = len(freqList)
    ImagFreqIgnored = lenF-lenI
    T = OFProc.getTemp()

    vibTemp = [1.98644568E-25 * 100 / 1.38064852E-23 * w for w in freqList]
    R = 8.314
    kBT = T * 1.38064852E-23 / 4.35974465E-18
    # Calculate thermal corrections, ignoring partition functions from translation and rotation, and vibration of heavy atoms
    q_elec = OFProc.getLog_q(2)

    q_rot = 0
    q_trans = 0

    # Translation
    St = (q_trans + 5/2.)*R
    Et = 3/2. *R*T

    # Rotation
    Sr = (q_rot + 3 / 2.) * R
    Er = 3/2.*R*T

    # Electronic (both are 0)
    Se = R*q_elec
    Ee = 0

    # Vibration
    Svk = [theta/T/(np.exp(theta/T)-1) - np.log(1-np.exp(-abs(theta)/T)) for theta in vibTemp]
    Evk = [theta * (0.5 + 1. / (np.exp(theta / T) - 1.)) for theta in vibTemp]

    Sv = R * sum(Svk)
    Ev = R * sum(Evk)
    # Thermal Corrections in Ha
    Ecorrection = (Et + Er + Ee + Ev) / 1000 / 2625.499638
    # Ha/K
    S = (St + Sr + Se + Sv) / 1000 / 2625.499638

    E = OFProc.getZeroPtEnergy()

    Ecorrected = E + Ecorrection

    constrainedH = Ecorrected + kBT
    constrainedTS = T * S
    constrainedG = constrainedH - constrainedTS
    return constrainedG,constrainedH,constrainedTS,ImagFreqIgnored