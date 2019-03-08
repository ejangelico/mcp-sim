import numpy as np 
import Field

#creating an electron. Currently looking at an E field in the x direction.
class Electron:
	def __init__(self, pos, vel = [0,0,0], acc = [0,0,0]):

		#Kinetmatic Variables

		#the mass units need to change as saving
		#numbers that are in the 10^-32 range is
		#not reliable from a computer memory standpoint. 
		#I would suggest working things out in terms of 
		#electron-volts and then having some functions that
		#solely do unit conversion math - constants being contained
		#in those functions
		self.mass = 9.10938356 * (10**(-31)) #kg
		self.charge = 1.60217662 * (10**(-19)) #Coulombs
		self.pos = pos
		self.vel = vel
		self.acc = acc

		#State variables
		self.last_pos = pos
		self.is_intersected = False

	
	def get_pos(self):
		return self.pos

	def get_lastpos(self):
		return self.last_pos

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

	
	#currently set up to propagate the kinematics through steps of dt
	#dt in nanoseconds
	def propagate(self, field, dt):
		#vector [x,y,z] field value
		Emag = field.get_magnitude(self.pos)

		self.acc[2] = (Emag[2]*self.charge)/self.mass
		self.last_pos = self.pos
		for i in range(3):
			self.vel[i] = self.vel[i] + self.acc[i]*dt
			self.pos[i] = self.pos[i] + self.vel[i]*dt

	
		
		







