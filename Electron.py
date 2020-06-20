import numpy as np 
import Field
import sys

global cc 
cc = 29.9792 #cm per ns
		

#creating an electron. Currently looking at an E field in the x direction.
class Electron:
	def __init__(self, pos, vel, acc, t_0):

		#Kinetmatic Variables

		#the mass units need to change as saving
		#numbers that are in the 10^-32 range is
		#not reliable from a computer memory standpoint. 
		#I would suggest working things out in terms of 
		#electron-volts and then having some functions that
		#solely do unit conversion math - constants being contained
		#in those functions
		self.mass = 511000 #eV/c^2
		self.pos = pos
		self.vel = vel
		self.acc = acc
		self.time = t_0 #current time in electrons frame
		self.last_pos_time = t_0 #stores time from the previous step in propagation

		#State variables
		self.last_pos = [0, 0, 0]
		#is it presently in the bulk of material
		self.is_intersected = False

		#this attribute stores the pore object
		#that the electron is presently in. 
		self.in_pore = None

	
	def get_pos(self):
		return self.pos

	def get_lastpos(self):
		return self.last_pos

	def get_time(self):
		return self.time

	def get_vel(self):
		return self.vel

	def get_in_pore(self):
		return self.in_pore


	def get_intersected(self):
		return self.is_intersected

	def set_intersected(self, a):
		self.is_intersected = a

	def set_in_pore(self, pore):
		self.in_pore = pore

	def set_pos(self, a):
		self.pos = a

	def set_lastpos(self, last_pos):
		self.last_pos = last_pos

	def set_time(self, time):
		self.time = time


	
	#currently set up to propagate the kinematics through steps of dt
	#dt in nanoseconds
	def propagate(self, mcp, field, dt, time):

		if(self.is_intersected==True):	#INTERPOLATE

			pore = self.in_pore #Gives us which pore object the electron is in
			angle = mcp.get_angle()  #get the bias angle

			#get the location info for our pore
			pore_center = pore.get_pore_center() #Centroid of pore
			R = pore.get_pore_radius()

			#Get atttributes of our electron in the mcp frame
			p0 = np.array(self.get_lastpos()) #electron position just before it stepped out of the pore, i.e. just before it broke the rules
			v = np.array(self.get_vel()) #the current velocity of the electron

			#Next we want to rotate into the pore frame such that the pores central axis is parallel to our new z' axis.
			#Define a passive rotation matrix about the x-axis
			theta = angle

			R_x = np.array([[1,         0,                  0                   ],
			                   [0,         np.cos(theta), np.sin(theta) ],
			                   [0,         -np.sin(theta), np.cos(theta)  ]
			                   ])




			#We will have to rotate our pore centroids into the pore frame
			pore_center_prime = np.dot(R_x, pore_center)
			x_cent = pore_center_prime[0]
			y_cent = pore_center_prime[1]

			#Rotate to get electron position in the pore frame coordinates
			p0 = np.dot(R_x, p0)

			#Electron velocity in the pore frame coordiantes
			v = np.dot(R_x, v)

			#To find the exact intersection location, we must first parameterize our interpolation line A(t) = p0 + dpt (pore frame).
			#Then we can look at the projection of this line onto a circle perpendicualr to the pore's axis. 
			#We then solve for t such that our interpolation line satisfies the equation of that circle. 
			#t is thus the time we must evolve our electron from its last position such that it is intersecting the pore wall
			
			#We parameterize our interpolation line and group coefficients by order of t
			second = v[0]**2 + v[1]**2 
			first = 2*p0[0]*v[0] - 2*x_cent*v[0] + 2*p0[1]*v[1] - 2*y_cent*v[1]
			const = p0[0]**2 + p0[1]**2 - 2*x_cent*p0[0] - 2*y_cent*p0[1] + x_cent**2 + y_cent**2 - R**2

			coeffs = [second, first, const]

			zeroes = (np.roots(coeffs)) #the np.roots function takes polynomial coeffs in descending order and returns solutions

			t = max(zeroes) #We take the positive time value

			p_intr = [p0[i] + v[i]*t for i in range(len(p0))] #we define the intersection point in pore frame coordinates
			
			#Then we need to rotate back into our lab frame
			theta = -theta

			R_x = np.array([[1,         0,                  0                   ],
			                   [0,         np.cos(theta), np.sin(theta) ],
			                   [0,         -np.sin(theta), np.cos(theta)  ]
			                   ])

			p_intr = np.dot(R_x, p_intr) 

			
			#Finally, we set the time and position attributes of our electron to the values found via interpolation
			self.set_time(t + self.last_pos_time)
			self.set_pos(p_intr)
			#print("landed at: \n", "pos: ", p_intr, "\n time: ", t + self.last_pos_time)
		# self.set_intersected(False)

			

		# #pseudocode:
		# #if(is_intersected is True):
		# #	find intersection point and time
		# # 	set the electron position/time to be that value	(interpolation)
		# #	*calculate absorption probability
		# #	*create secondary electrons if needed
		# #	calculate scattering angle and new velocity
		# #	is_intersected = False
		# #
		# #propagate once 
		else:
			#vector [x,y,z] field value
			Emag = field.get_field_vector(self.pos) # V/cm

			self.acc = [(_*cc*cc*10000.0)/self.mass for _ in Emag] #micron/ns**2
			for i in range(len(self.vel)):
				self.last_pos[i] = self.pos[i]
				self.vel[i] = self.vel[i] + self.acc[i]*dt
				self.pos[i] = self.pos[i] + self.vel[i]*dt
				self.time = time + dt
				self.last_pos_time = time








