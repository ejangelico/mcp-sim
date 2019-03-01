import numpy as np 
import Field

#creating an electron. Currently looking at an E field in the x direction.
class Electron:
	def __init__(self, pos_x, pos_y, pos_z, vel_x = None, vel_y = None, vel_z = None):
		self.mass = 9.10938356 * (10**(-31)) #kg
		self.charge = 1.60217662 * (10**(-19)) #Coulombs
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.pos_z = pos_z
		self.vel_x = 0
		self.vel_y = 0
		self.vel_z = 0
		self.a_x = 1
		self.a_y = 1
		self.a_z = 1
	

	def get_pos_x(self):
		return self.pos_x

	def get_pos_y(self):
		return self.pos_y

	def get_pos_z(self):
		return self.pos_z

	def get_vel_x(self):
		return self.vel_x

	def get_vel_y(self):
		return self.vel_y

	def get_vel_z(self):
		return self.vel_z
	
	#currently set up to propagate the kinematics through steps of dt
	def propagate(self, E, dt):
		self.a_z = (E*self.charge)/self.mass
		self.vel_x = self.vel_x + self.a_x*dt
		self.vel_y = self.vel_y + self.a_y*dt
		self.vel_z = self.vel_z + self.a_z*dt

		self.pos_x = self.pos_x + self.vel_x*dt
		self.pos_y = self.pos_y + self.vel_y*dt
		self.pos_z = self.pos_z + self.vel_z*dt

	
		
		







