import numpy as np 
import Electron
import Field
import Mcp
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import sys

# generate random electrons with random positions
electrons=[]

for i in range(100):
	pos = (4*((2*np.random.rand(3))-1))
	electron=Electron.Electron(pos[0], pos[1], pos[2])
	electrons.append(electron)

#create E field
field = Field.Field()
E = field.get_magnitude()

#create an Mcp instance. Requires parameters: pore radius, square dimension, pore spacing
my_mcp=Mcp.Mcp(0.1, 4, 0.25)

while len(electrons) != 0:  #will run until every electron has hit a wall (i.e. is outside a pore)
	for e in electrons:
		in_pore = my_mcp.check_intersection(e) #checks to see if electon is still in a pore
		if in_pore == True:
			e.propagate(E, 0.5) #the propagate functionrequires the params: field magnitude, time step. Currently only in z direction.

		else:
			print(f'Intersected at r = ({e.pos_x:.2f},{e.pos_y:.2f},{e.pos_z:.2f})') #location of e when it is outside of pore
			electrons.remove(e)



sys.exit()
"""
#radius of pore
r = .1

#empty list that will contain our electrons
electrons=[]

#creates a specified number of electron objects with position components sampled from specified range of random floats
for i in range(100):
	pos = (4*((2*np.random.rand(3))-1))
	electron=Electron(pos[0], pos[1], pos[2])
	electrons.append(electron)	

#plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-4, 4])

#defines range of pore central axis locations and spacing of pores (currently pores spaced from [-4, 4) on x and y
pore_x_space=np.arange(-4,4,0.5)
pore_y_space=np.arange(-4,4,0.5)

#not operational since I dont know how to sample the distribution of events
for electron in electrons:
	for pore_x in pore_x_space:
		for pore_y in pore_y_space:
			if (electron.get_pos_x() - pore_x)**2 + ((electron.get_pos_y() - pore_y) + ((electron.get_pos_z())*np.sin(np.pi/5)))**2 <= r**2:
				#ax.scatter(electron.get_pos_x(), electron.get_pos_y(), electron.get_pos_z(), s=1, color='k')
				sample the thing
			else:
				propagate(electron)
			


plt.show()
"""

