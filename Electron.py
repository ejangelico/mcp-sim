import numpy as np 


#creating an electron. Currently looking at an E field in the x direction.
class Electron:
	def __init__(self, pos_x, pos_y, pos_z):
		e_field = 10 #N/C
		self.mass = 9.10938356 * (10**(-31)) #kg
		self.charge = 1.60217662 * (10**(-19)) #Coulombs
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.pos_z = pos_z
		self.vel_x = 0
		#self.vel_y = vel_y
		#self.vel_z = vel_z
		self.a_x = (self.charge*e_field)/self.mass
	
	#currently set up to propagate the kinematics through steps of dt for time t=duration
	def propagate(self, duration):
		self.duration=duration
		t = 0
		dt = 0.001
		while (t<duration):
			self.pos_x = self.pos_x + self.vel_x*dt
			self.vel_x = self.vel_x + self.a_x*(dt)
			t+=dt
			



