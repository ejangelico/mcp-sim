import numpy as np 


class Field:
	def __init__(self, const_mag):
		self.const_mag = const_mag #volts/cm

	def get_magnitude(self, pos):
		#returns vector field values
		return [0, 0, self.const_mag]

