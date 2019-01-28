import numpy as np 
from Electron import Electron
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import sys

#radius of pore
r = .1

#empty list that will contain our electrons
electrons=[]

#creates a specified number of electron objects with position components sampled from specified range of random floats
for i in range(1000):
	pos = (4*((2*np.random.rand(3))-1))
	print(pos)
	electron=Electron(pos[0], pos[1], pos[2])
	electrons.append(electron)	

#plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-4, 4])

#defines range of pore central axis locations and spacing of pores (currently only one row of pores)
pore_space=np.arange(-4,4,0.5)

for electron in electrons:
	for pore in pore_space:
		if (electron.pos_x - pore)**2 + ((electron.pos_y) + ((electron.pos_z)*np.sin(np.pi/5)))**2 <= r**2:
			ax.scatter(electron.pos_x, electron.pos_y, electron.pos_z, s=1, color='k')


plt.show()

