import numpy as np 
import Electron
import Field
import Mcp
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import sys
import time


def create_random_electrons(nelec, xyrange, z):
	# generate random electrons with random positions
	electrons=[]

	for i in range(nelec):
		#random dist of electrons between -1000 and 1000 microns all at z=5e5 microns
		pos = [np.random.uniform(xyrange[0], xyrange[1]), np.random.uniform(xyrange[0], xyrange[1]), z]
		electron=Electron.Electron(pos, [0,0,0],[0,0,0])
		electrons.append(electron)

	return electrons


def evolve_elecs(el, mcp, E):
	timestep = 0.005 #nanoseconds
	endtime = 1 #nanoseconds
	curtime = 0
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	while True:
		if(int(curtime*1000) % 100 == 0):
			print "evolved to time " + str(curtime) + " ns"

		if(curtime > endtime):
			break

		for e in el:
			in_bulk = my_mcp.is_electron_in_bulk(e) #checks to see if electon has propagated inside the bulk of the MCP
			if(in_bulk == False):
				e.propagate(field, timestep) #the propagate functionrequires the params: field object, time step. Currently only in z direction.


			else:
				e.set_intersected(True)

		curtime += timestep
		

	mcp.plot_pores(ax)
	plot_all_elecs(el, ax)
	plt.show()
	#zs = [e.get_pos()[2] for e in el]
	#fig, ax = plt.subplots()
	#ax.hist(zs)
	#plt.show()

def plot_all_elecs(el, ax = None):
	if(ax is None):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

	for e in el:
		p = e.get_pos()
		ax.scatter(p[0], p[1], p[2], c='k')

	

if __name__ == "__main__":
	el = create_random_electrons(1000, [-100,100], 15)


	#create E field
	field = Field.Field(-200)

	#create an Mcp instance. Requires parameters: pore radius, square dimension, pore spacing
	mcpthick = 1000. #um
	pore_rad = 40. #um
	pore_space = 2*pore_rad + 3 #um
	mcplength = 0.060 #mm
	pore_bias = 8. #degrees
	top_z_coord = 0 #um
	my_mcp=Mcp.Mcp(pore_rad, mcplength, pore_space, top_z_coord, mcpthick, pore_bias)

	evolve_elecs(el, my_mcp, field)
	plot_all_elecs(el)





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




