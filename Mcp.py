import numpy as np 
import Field
import Electron



class Mcp:
	def __init__(self, pore_rad, square_dim, pore_space):
		self.pore_rad = pore_rad #radius of pore in cm
		self.square_dim = square_dim #dimension of the square MCP
		self.pore_space = pore_space #space between each pore
		#geometry is weird, but right now we have a square mcp with pores at the very edges
		self.x_pores = np.arange(-self.square_dim, self.square_dim + self.pore_space, self.pore_space) # creates central axes of pores along x axis
		self.y_pores = np.arange(-self.square_dim, self.square_dim +self.pore_space, self.pore_space) # creates central axes of pores along y axis




	def check_intersection(self, electron):
		#defines radius of the pore as specified for the instance
		r = self.pore_rad

		for pore_x in self.x_pores:
			for pore_y in self.y_pores:
				if (electron.get_pos_x() - pore_x)**2 + ((electron.get_pos_y() - pore_y) + ((electron.get_pos_z())*np.sin(np.pi/5)))**2 <= r**2:
					#ax.scatter(electron.get_pos_x(), electron.get_pos_y(), electron.get_pos_z(), s=1, color='k')
					return True

				else:
					False