import config
import mod
import cmath
import numpy as np
import re
config.outputFileName = "C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/C2H4opt.log"
config.inputFileName = 'C:/Users/Craig/PycharmProjects/g09-Python-Processing/testFiles/C2H4opt.gjf'

mod.setN()
mod.setN_Freeze()

import IFProc
import OFProc

masses = np.array(OFProc.getMasses())
coords = OFProc.getOptCoords()

# D1 = [x for pair in zip(masses,0,0) for x in pair]
# D2 = [x for pair in zip(0,masses,0) for x in pair]
# D3 = [x for pair in zip(0,0,masses) for x in pair]

coords = OFProc.getOptCoords()

# Strip \n
coords = map(str.strip, coords)
# Split up each row into list
coords = map(lambda x: x.split(), coords)
coords = np.asmatrix([[(float(j)) for j in i] for i in coords])
# Calculate center of mass
CoM = np.dot(masses,coords)/sum(masses)
CoM = np.ndarray.tolist(CoM)

# Shift origin to COM
centeredCoords = np.zeros((3,3))
# squeezing and as array because I am bad at Python
centeredCoords = np.squeeze(np.asarray([np.subtract(coords[x],CoM).flatten() for x in range(config.N)]))


# print coords
inertiaTensor = np.zeros((3,3))

# Diagonal elements
inertiaTensor[0,0] = np.sum(np.multiply(masses,(centeredCoords[:,1]**2+centeredCoords[:,2]**2)))
inertiaTensor[1,1] = np.sum(np.multiply(masses,(centeredCoords[:,0]**2+centeredCoords[:,2]**2)))
inertiaTensor[2,2] = np.sum(np.multiply(masses,(centeredCoords[:,1]**2+centeredCoords[:,0]**2)))

# Off diagonals
inertiaTensor[1,0] = -np.sum(np.multiply(np.multiply(masses,centeredCoords[:,1]),centeredCoords[:,0]))
inertiaTensor[0,1] = inertiaTensor[1,0]
inertiaTensor[2,0] = -np.sum(np.multiply(np.multiply(masses,centeredCoords[:,2]),centeredCoords[:,0]))
inertiaTensor[0,2] = inertiaTensor[2,0]
inertiaTensor[2,1] = -np.sum(np.multiply(np.multiply(masses,centeredCoords[:,2]),centeredCoords[:,1]))
inertiaTensor[1,2] = inertiaTensor[2,1]
# Inertia tensor in AMU Ang**2 --> AMU Bohr**2
inertiaTensor = np.multiply(inertiaTensor,1./0.52917721067**2)
# Calcualte evals in AMU Bohr**2
evals,evecs = np.linalg.eig(inertiaTensor)

# print evals
# print evecs
# print masses

D1 = np.zeros(3*config.N)
D2 = np.zeros(3*config.N)
D3 = np.zeros(3*config.N)
for x in range(config.N):
    D1[3*x] = D1[3*x]+masses[x]
D2 = np.roll(D1,1)
D3 = np.roll(D1,2)
print centeredCoords[0]

D4 = np.zeros((config.N,3))
D5 = D4
D6 = D4
print evecs
print centeredCoords[0]
for i in range(1):
    Px = np.dot(centeredCoords[i], evecs[0])
    Pz = np.dot(centeredCoords[i], evecs[1])
    Py = np.dot(centeredCoords[i], evecs[2])

    print Px,Pz,Py
    for j in range(3):
        # print j
        D4[i,j] = (Py*evecs[j,2]-Pz*evecs[j,1])/masses[i/3]
        D5[i,j] = (Pz*evecs[j,0]-Px*evecs[j,2])/masses[i/3]
        D6[i,j] = (Px*evecs[j,1]-Py*evecs[j,0])/masses[i/3]

# print D4
# print D4.flatten()
print D4