import numpy as np 
import Field
import Electron



class Mcp:
	def __init__(self, pore_rad, mcp_length, pore_spacing, top_z_coord, thickness=1000, angle=0):
		self.pore_rad = pore_rad #radius of pore in micron
		self.angle = angle*np.pi/180.0 #angle of pores in radians
		self.mcp_length = mcp_length #length of one side of the MCP in mm
		self.pore_spacing = pore_spacing #space between each pore in microns
		self.thickness = thickness #thickness of MCP in z dimension in micron
		self.top_z_coord = top_z_coord 


		#geometry is weird, but right now we have a square mcp with pores at the very edges
		#mcp_length multiplied by a factor of 1000 such that these x-y coordinates are in microns
		self.x_pores = np.arange(-0.5*self.mcp_length*1000, 0.5*self.mcp_length*1000 + self.pore_spacing, self.pore_spacing) # creates central axes of pores along x axis
		self.y_pores = np.arange(-0.5*self.mcp_length*1000, 0.5*self.mcp_length*1000 +self.pore_spacing, self.pore_spacing) # creates central axes of pores along y axis
		self.z_bounds = [top_z_coord - thickness, top_z_coord]


	def plot_pores(self, ax = None):
		if(ax is None):
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')

		for pore_x in self.x_pores:
			for pore_y in self.y_pores:
				#define a line that is the cylinder's axis.
				#p1 and p2 are two points on the line
				p0 = np.array([pore_x, pore_y + 0.5*self.thickness*np.tan(self.angle), self.top_z_coord - self.thickness]) #center of pore
				p1 = np.array([pore_x, pore_y - 0.5*self.thickness*np.tan(self.angle), self.top_z_coord]) #pore top with angle shift

				R = self.pore_rad
				#vector in direction of axis
				v = p1 - p0
				#find magnitude of vector
				mag = np.linalg.norm(v)
				#unit vector in direction of axis
				v = v / mag
				#make some vector not in the same direction as v
				not_v = np.array([1, 0, 0])
				if (v == not_v).all():
				    not_v = np.array([0, 1, 0])
				#make vector perpendicular to v
				n1 = np.cross(v, not_v)
				#normalize n1
				n1 /= np.linalg.norm(n1)
				#make unit vector perpendicular to v and n1
				n2 = np.cross(v, n1)
				#surface ranges over t from 0 to length of axis and 0 to 2*pi
				#
				t = np.linspace(0, mag, 100)
				theta = np.linspace(0, 2 * np.pi, 100)
				#use meshgrid to make 2d arrays
				t, theta = np.meshgrid(t, theta)
				#generate coordinates for surface
				X, Y, Z = [p0[i] + v[i] * t + R * np.sin(theta) * n1[i] + R * np.cos(theta) * n2[i] for i in [0, 1, 2]]
				ax.plot_surface(X, Y, Z, alpha=0.3)
				#plot axis
				ax.plot(*zip(p0, p1), color = 'red')





	def is_electron_in_bulk(self, electron):

		#safety check, is it already defined to be intersected?
		if(electron.get_intersected()):
			return True

		#defines radius of the pore as specified for the instance
		r = self.pore_rad

		in_vacuum = False #assume guilty before proving innocent

		for pore_x in self.x_pores:
			for pore_y in self.y_pores:
				#if it is not even in the z bounds of the MCP
				if(electron.get_pos()[2] > max(self.z_bounds) or electron.get_pos()[2] < min(self.z_bounds)):
					in_vacuum = True

				#define a line that is the cylinder's axis.
				#p1 and p2 are two points on the line
				p1 = [pore_x, pore_y, self.top_z_coord - 0.5*self.thickness] #center of pore
				p2 = [pore_x, pore_y - 0.5*self.thickness*np.tan(self.angle), p1[2] + 0.5*self.thickness] #pore top with angle shift
				p0 = electron.get_pos()

				p01 = [p0[i] - p1[i] for i in range(len(p1))]
				p02 = [p0[i] - p2[i] for i in range(len(p2))]
				p21 = [p2[i] - p1[i] for i in range(len(p1))]

				cross_term = np.cross(p01,p02)
				cross_mag = np.linalg.norm(cross_term)
				denom = np.linalg.norm(p21)

				#the "point line distance" theorem in 
				#http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
				#gives a representation of a cylinder. Equation 10, where d is the radius
				#of the cylinder. 

				if(cross_mag/denom < r):
					in_vacuum = True

		#check if it survived checks
		if(in_vacuum):
			return False
		else:
			return True

