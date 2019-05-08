import numpy as np 


class Field:
	def __init__(self, const_mag):
		self.const_mag = const_mag #V / cm

	def get_field_vector(self, pos):
		#returns vector field values
		return [0, 0, self.const_mag]

