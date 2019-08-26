import numpy as np 
import Field
import Mcp
import Electron

class Pore:
	def __init__(self, pos, center, axis, angle, radius):
		self.pos = pos
		self.center = center
		self.axis = axis
		self.angle = angle
		self.radius = radius

	def get_pore_pos(self):
		return self.pos

	def get_pore_center(self):
		return  self.center

	def get_pore_axis(self):
		return self.axis

	def get_pore_radius(self):
		return self.radius
