import numpy as np 
import Electron
import Field
import Mcp
import Pore
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
			my_mcp.check_in_pore(e) #checks to see if electon has propagated inside the bulk of the MCP
			e.propagate(field, timestep) #the propagate functionrequires the params: field object, time step. Currently only in z direction.


		#if all electrons are at z = -5 or 
		#one electron reaches t = 5 ns then break
		

	mcp.plot_pores(ax)
	plot_all_elecs(el, ax)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
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


def interpolate(electron, mcp, pore):
	pore_pos = pore.get_pore_pos()
	A = pore.get_pore_axis()
	#First we need to find the intersection between the interpolation line and the cylindrical pore
	pore_center = [pore_pos[0], pore_pos[1], mcp.top_z_coord - 0.5*mcp.thickness] #this is the center of the pore
	pore_top = [pore_pos[0], pore_pos[1] - 0.5*mcp.thickness*np.tan(mcp.angle), pore_center[2] + 0.5*mcp.thickness] #This is the top of pore on axis

	A = [pore_top[i] - pore_center[i] for i in range(3)] #This is the central axis of the pore

	p0 = electron.get_lastpos()
	p1 = electron.get_pos()

	#We first will find the projection of the interpolation vector onto a plane orthogonal to the cylinder using:
	#https://math.stackexchange.com/questions/2126565/intersection-between-a-cylinder-and-a-given-line

	term1 = [p1[i] - p0[i] for i in range(3)] #This is the vector from last_pos to pos
	term2 = [A[i] - p0[i] for i in range(3)] #Term in formula
	term3 = [A[i] - p0[i] for i in range(3)] #Term in formula

	cross_term = np.cross(term1, term2)
	cross_mag = np.linalg.norm(cross_term)
	denom = np.linalg.norm(term3)

	orthog_proj = cross_mag/denom

	dpos = np.asarray(term1) #Renaming for clarity: dpos = pos - lastpos

	pos_intr = p0 + (R/orthog_proj)*(dpos) #This is the point of intersection

	#Now we can solve to find the time of intersection

	d = np.linalg.norm(pos_intr - p0) #Magnitude of vector from lastpos to point of intersection

	dp = [p1[i] - p0[i] for i in range(3)] #Slopes so we can parameterize our interpolation line

	#Next we write parameterized line as a vector v = (r_0 + dr*t), take its magniutde and set that equal to the distance between lastpos and intersection point. 
	#Writing the resulting polynomial in standard form and then putting coefficients into a list we get:
	coeffs = [dp[0]**2 + dp[1]**2 + dp[2]**2, 2*(p0[0]*dp[0] + p0[1]*dp[1] + p0[2]*dp[2]), p0[0]**2 + p0[1]**2 + p0[2]**2 - d**2]

	#numpy gives us the roots, which in this case is the time between lastpos and intersection point
	roots = np.roots(coeffs)

	t = roots[roots > 0] #Take the positive root
	t = t[0] #And now we have the time between last_pos and point of intersection

	

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




