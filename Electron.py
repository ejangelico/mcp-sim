import numpy as np 
import Field
import sys

global cc 
cc = 29.9792 #cm per ns
		

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
		self.mass = 511000 #eV
		self.pos = pos
		self.vel = vel
		self.acc = acc
		self.time = 0 #current time in electrons frame

		#State variables
		self.last_pos = pos
		#is it presently in the bulk of material
		self.is_intersected = False

		#this attribute stores the pore object
		#that the electron is presently in. 
		self.in_pore = None

	
	def get_pos(self):
		return self.pos

	def get_lastpos(self):
		return self.last_pos

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


	
	#currently set up to propagate the kinematics through steps of dt
	#dt in nanoseconds
	def propagate(self, field, dt):

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


		#vector [x,y,z] field value
		Emag = field.get_field_vector(self.pos) # V/cm

		self.acc = [(_*cc*cc*10000.0)/self.mass for _ in Emag] #micron/ns**2
		self.last_pos = self.pos
		for i in range(len(self.vel)):
			self.vel[i] = self.vel[i] + self.acc[i]*dt
			self.pos[i] = self.pos[i] + self.vel[i]*dt

	
		
		







