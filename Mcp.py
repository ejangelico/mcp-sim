import numpy as np 
import Field
import Electron



class Mcp:
	def __init__(self, pore_rad, mcp_length, pore_spacing, top_z_coord, thickness=1000, angle_x=0, angle_y=0):
		self.pore_rad = pore_rad #radius of pore in micron
		self.angle_x = angle_x #angle of pores in degrees in the x dimension
		self.angle_y = angle_y #angle of pores in degrees in the y dimension
		self.mcp_length = mcp_length #length of one side of the MCP in mm
		self.pore_spacing = pore_spacing #space between each pore in microns
		self.thickness = thickness #thickness of MCP in z dimension in micron
		self.top_z_coord = top_z_coord 


		#geometry is weird, but right now we have a square mcp with pores at the very edges
		#mcp_length multiplied by a factor of 1000 such that these x-y coordinates are in microns
		self.x_pores = np.arange(-0.5*self.mcp_length*1000, 0.5*self.mcp_length*1000 + self.pore_spacing, self.pore_spacing) # creates central axes of pores along x axis
		self.y_pores = np.arange(-0.5*self.mcp_length*1000, 0.5*self.mcp_length*1000 +self.pore_spacing, self.pore_spacing) # creates central axes of pores along y axis
		self.z_bounds = [top_z_coord - thickness, top_z_coord]


	def is_electron_in_bulk(self, electron):

		if(electron.get_pos_z() > 0):
			return False

		else:
			return True

"""
		#safety check, is it already defined to be intersected?
		if(electron.get_intersected()) == True:
			return True

		#defines radius of the pore for specific Mcp object

		radius = self.pore_rad

		for pore_x in self.x_pores:
			for pore_y in self.y_pores:

				if(electron.get_pos_z() < 0):
					return True
				#if it is not even in the z bounds of the MCP
				if(electron.get_pos_z() > max(self.z_bounds)):
					return False


				#if it is inside of one of the pores but has not 
				#entered the bulk of the MCP
				if (electron.get_pos_x() - pore_x)**2 + ((electron.get_pos_y() - pore_y) + ((electron.get_pos_z())*np.sin(np.pi/5)))**2 <= radius**2:
					#ax.scatter(electron.get_pos_x(), electron.get_pos_y(), electron.get_pos_z(), s=1, color='k')
					return False

				else:
					True

"""