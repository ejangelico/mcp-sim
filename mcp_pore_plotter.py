import numpy as np 
import Electron
import Field
import Mcp
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import sys
import time

# generate random electrons with random positions
electrons=[]

for i in range(100):
	xyrange = [-1000, 1000]
	#random dist of electrons between -1000 and 1000 microns all at z=5e5 microns
	pos = [np.random.uniform(xyrange[0], xyrange[1]), np.random.uniform(xyrange[0], xyrange[1]), 5e5]
	electron=Electron.Electron(pos)
	electrons.append(electron)

#create E field
field = Field.Field(2)

#create an Mcp instance. Requires parameters: pore radius, square dimension, pore spacing
mcpthick = 1000. #um
pore_rad = 10. #um
pore_space = pore_rad + 3 #um
mcplength = 33. #mm
pore_bias_x = 8. #degrees
pore_bias_y = 0. #degrees
top_z_coord = 1e4 #um
my_mcp=Mcp.Mcp(pore_rad, mcplength, pore_space, mcpthick, pore_bias_x, pore_bias_y)


timestep = 0.01 #nanoseconds
endtime = 2 #nanoseconds
curtime = 0
while True:
	if(int(curtime*1000) % 100 == 0):
		print "evolved to time " + str(curtime) + " ns"

	if(curtime > endtime):
		break

	for e in electrons:
		in_bulk = my_mcp.is_electron_in_bulk(e) #checks to see if electon has propagated inside the bulk of the MCP
		if in_bulk == False:
			e.propagate(field, timestep) #the propagate functionrequires the params: field object, time step. Currently only in z direction.

		else:
			e.set_intersected(True)

	curtime += timestep



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

