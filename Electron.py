import numpy as np 
import Field

global cc
cc = 299792 #um/ns

#creating an electron. Currently looking at an E field in the x direction.
class Electron:
	def __init__(self, pos, vel, acc):

		#Kinetmatic Variables

		#the mass units need to change as saving
		#numbers that are in the 10^-32 range is
		#not reliable from a computer memory standpoint. 
		#I would suggest working things out in terms of 
		#electron-volts and then having some functions that
		#solely do unit conversion math - constants being contained
		#in those functions
		self.mass = 511000 #eV/c^2
		self.pos = pos #um
		self.vel = vel #um/ns
		self.acc = acc #um/ns^2
		self.local_time = 0
		#State variables
		self.last_pos = pos
		self.is_intersected = False

	
	def get_pos(self):
		return self.pos

	def get_lastpos(self):
		return self.last_pos

	def get_local_time(self):
		return self.local_time

	def get_vel(self):
		return self.vel

	def get_pos_x(self):
		return self.pos[0]

	def get_pos_y(self):
		return self.pos[1]

	def get_pos_z(self):
		return self.pos[2]

	def get_vel_x(self):
		return self.vel[0]

	def get_vel_y(self):
		return self.vel[1]

	def get_vel_z(self):
		return self.vel[2]

	def get_intersected(self):
		return self.is_intersected

	def set_intersected(self, a):
		self.is_intersected = a

	def set_pos(self, p):
		self.pos = p


	
	#currently set up to propagate the kinematics through steps of dt
	#dt in nanoseconds
	def propagate(self, f, dt):
		#vector [x,y,z] field value
		Emag = f.get_magnitude(self.pos) 

		self.acc[2] = cc*cc* 1e-4 * (Emag[2]/self.mass) #1/um
		self.last_pos = self.pos
		for i in range(3):
			self.vel[i] = self.vel[i] + self.acc[i]*dt
			self.pos[i] = self.pos[i] + self.vel[i]*dt

			
			


	
		
		







