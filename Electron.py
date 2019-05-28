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
		self.mass = 511000 #eV
		self.pos = pos
		self.vel = vel
		self.acc = acc
		self.time = t_0 #current time in electrons frame

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

	def set_pos(self, pos):
		self.pos = pos

	def set_lastpos(self, last_pos):
		self.last_pos = last_pos

	def set_time(self, time):
		self.time = time


	
	#currently set up to propagate the kinematics through steps of dt
	#dt in nanoseconds
	def propagate(self, mcp, field, dt):

		thickness = 500

		if(self.is_intersected==True):
			#INTERPOLATE
			pore = self.in_pore #Gives us which pore object the electron is in
			angle = mcp.get_angle() 
			if(pore ==None):
				return False
			#Tet the location info for our pore
			pore_pos = pore.get_pore_pos() #Centroid of pore
			print "pore pos is: ", pore_pos
			x_pore = pore_pos[0] #Break it out for later
			y_pore = pore_pos[1] - 0.5*thickness*np.tan(angle)
			R = pore.get_pore_radius()

			#Get the location info for our electron in the mcp frame
			p0 = np.array(self.get_lastpos()) #before el left the pore
			p1 = np.array(self.get_pos()) #after el left the pore

			dp1 = p1 - p0

			print "inter vec pre rotation: ", dp1

			#This is a passive rotation matrix. 
			#We rotate into a pore frame such that the pores axis is parallel to z' axis.
			theta = angle

			R_x = np.array([[1,         0,                  0                   ],
			                   [0,         np.cos(theta), np.sin(theta) ],
			                   [0,         -np.sin(theta), np.cos(theta)  ]
			                   ])



			#We will have to rotate our pore centroids into the pore frame
			y_pore = y_pore * np.cos(theta)
			x_pore = x_pore


			#Electron positions in the pore frame
			p0 = np.dot(R_x, p0)
			p1 = np.dot(R_x, p1)

			#Interpolation vector in the pore frame.
			dp = p1-p0

			print "inter vec: ", dp

			#To find the exact intersection location, we must first parameterize our interpolation line A(t) = p0 + dpt (pore frame).
			#Then we can look at the projection of this line onto a circle perpendicualr to the pore's axis. 
			#We then set the magnitude of this projection equal to the radius of our pore and solve for the free parameter t.
			#The np.roots function requires our polynomial to be in standard form in order to solve for t. 
			#I have separated out the expression by order of t. 
			const = p0[0]**2 + p0[1]**2 + y_pore**2 + x_pore**2 - 2*p0[0]*x_pore - 2*p0[1]*y_pore - R**2

			first = 2*dp[0]*p0[0] + 2*dp[1]*p0[1] - 2*dp[0]*x_pore - 2*dp[1]*y_pore 

			second = dp[0]**2 + dp[1]**2

			coeffs = [second, first, const]

			print coeffs

			roots = np.roots(coeffs)

			print roots, "roots"

			t = roots[roots > 0]
			print "time is: ", t

			#Now we can evaluate our interpolation line at the appropriate value of t.
			#This gives us the point of intersection in the pore frame.
			p_intr = p0 + dp*t


			theta = -1* theta 

			R_x = np.array([[1,         0,                  0                   ],
			                   [0,         np.cos(theta), np.sin(theta) ],
			                   [0,         -np.sin(theta), np.cos(theta)  ]
			                   ])

			#Finally, we express the point of intersection in our lab frame by passively rotating back the way we came. 
			p_intr = np.dot(R_x, p_intr)

			self.set_time(t)
			self.set_pos(p_intr)

			

		#pseudocode:
		#if(is_intersected is True):
		#	find intersection point and time
		# 	set the electron position/time to be that value	(interpolation)
		#	*calculate absorption probability
		#	*create secondary electrons if needed
		#	calculate scattering angle and new velocity
		#	is_intersected = False
		#
		#propagate once 
		else:
			#vector [x,y,z] field value
			Emag = field.get_field_vector(self.pos) # V/cm

			self.acc = [(_*cc*cc*10000.0)/self.mass for _ in Emag] #micron/ns**2
			for i in range(len(self.vel)):
				self.vel[i] = self.vel[i] + self.acc[i]*dt
				self.pos[i] = self.pos[i] + self.vel[i]*dt

			for i in range(len(self.pos)):
				self.last_pos[i] = self.pos[i] - self.vel[i]*dt

			if(self.last_pos[2] == self.pos[2]):
				print "last position is same as position \n"





