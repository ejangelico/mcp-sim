import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import sys
import time



#Interpolation function


# lastpos = np.array([0,0,0])

# pos = np.array([0,0,5])

# d = 3

# x_0 = lastpos[0]
# y_0 = lastpos[1]
# z_0 = lastpos[2]

# dx = pos[0] - lastpos[0]
# dy = pos[1] - lastpos[1]
# dz = pos[2] - lastpos[2]

# p0 = lastpos
# p1 = pos 


# dp=[p1[i] - p0[i] for i in range(3)]


# coeffs = [dx**2 + dy**2 + dz**2 , 2*(x_0*dx + y_0*dy + z_0*dz), x_0**2 + y_0**2 + z_0**2 - d**2] 
# coeffs1 = [dp[0]**2 + dp[1]**2 + dp[2]**2, 2*(p0[0]*dp[0] + p0[1]*dp[1] + p0[2]*dp[2]), p0[0]**2 + p0[1]**2 + p0[2]**2 - d**2]
# t[ ]

# roots = np.roots(coeffs)
# roots1 = np.roots(coeffs1)

# t = roots[roots > 0]
# t=t[0]

# t1 = roots1[roots1 > 0]
# t1 = t1[0]

# pos_intr = [x_0 + dx*t, 
# 			y_0 + dy*t, 
#  			z_0 + dz*t]

# pos1_intr = [x_0 + dx*t, 
# 			y_0 + dy*t, 
#  			z_0 + dz*t]


# print "long form", pos_intr, "short form", pos1_intr



#OK TRY AGAIN BIOTCH
#following the nerds at:
#https://math.stackexchange.com/questions/2126565/intersection-between-a-cylinder-and-a-given-line

# R = 2. #radius heuristic

#A = [pore_x, pore_y - 0.5*self.thickness*np.tan(self.angle), p1[2] + 0.5*self.thickness] #pore top

# A = np.array([0., 0., 10.])
# B = np.array([0,0,0])

# lastpos = [0., 0., 0.]
# pos = [0., 4., 0.]

# p1 = np.asarray(pos) #position outside of pore that triggered interpolation fn
# p0 = np.asarray(lastpos) #last position of electron inside the pore

# term1 = np.linalg.norm(A - B)
# term2 = p1 - p0
# term3 = A - p0

# cross_term = np.cross(term2, term3)
# cross_mag = np.linalg.norm(cross_term)

# scale_term = term1 / cross_mag


# pos_intr = p0 + (R * scale_term) * term2  #so now we have the intersection point but we still need the time of that intersection

# print(pos_intr)

# theta = np.pi/4

# R_x = np.array([[1,         0,                  0                   ],
#                    [0,         np.cos(theta), -np.sin(theta) ],
#                    [0,         np.sin(theta), np.cos(theta)  ]
#                    ])

# #Now let's try satisfying the eq for a tilted cylinder
# R = 2
# p0 = np.array([0, 0, 0])
# p1 = np.array([0, 4, 0])

# p0 = np.dot(R_x, p0)
# p1 = np.dot(R_x, p1)

# dp = p1 - p0




# coeffs = [dp[0]**2 + dp[1]**2, 2*p0[0]*dp[0] + 2*p0[1]*dp[1], p0[0]**2 + p0[1]**2 - R**2] 

# sols = np.roots(coeffs)

# t = sols[sols > 0]

# p_intr = np.array(p0 + dp*t)


# print("time: ", t, "\n", "intersection: ", p_intr)

#************************************************************Hard Code
# R = 2
# theta = np.pi/4

# x_pore = 0
# y_pore = 0

# p0 = np.array([-1,0,0])
# p1 = np.array([-4, 0, 0])
# dp = p1-p0

# second = dp[0]**2 + dp[1]**2 - 2*dp[1]*dp[2]*np.sin(theta) + dp[2]**2 * np.sin(theta)**2
# first = 2*dp[0]*p0[0] - 2*dp[0]*x_pore - 2*dp[1]*p0[2] + 2*dp[2]*np.sin(theta)*p0[2] + 2*dp[1]*p0[1]
# const = p0[0]**2 + p0[1]**2 + p0[2]**2 - 2*dp[2]*np.sin(theta)*p0[1] - 2*dp[1]*y_pore + 2*dp[2]*np.sin(theta)*y_pore - 2*p0[1]*y_pore + y_pore**2 - 2*p0[1]*p0[2] + 2*y_pore*p0[2] - 2*p0[0]*x_pore + x_pore**2 - R**2

# coeffs1 = [second, first, const]

# sols1 = np.roots(coeffs1)
# sols1 = sols1[sols1 > 0]

# p_intr1 = p0 + dp*sols1

# print(p_intr1)



#************************************** Now Just Try Rotating into Frame of Cylinder

#Let's define a pore with radius R rotated about the x-axis by angle theta
R = 2
theta = np.pi/4

#This is a passive rotation matrix. 
#We rotate into a pore frame such that the pores axis is parallel to z' axis.
R_x = np.array([[1,         0,                  0                   ],
                   [0,         np.cos(theta), np.sin(theta) ],
                   [0,         -np.sin(theta), np.cos(theta)  ]
                   ])


#Define the centroid of our pore
x_pore = 50
y_pore = 50

#We will have to transform our pore centroids as we rotate about the x-axis
y_pore = y_pore * np.cos(theta)
x_pore = x_pore

#Electron positions in the lab frame
p0 = np.array([50, 50, 0])
p1 = np.array([50, 559, 0])

#Electron positions in the rotated frame
p0 = np.dot(R_x, p0)
p1 = np.dot(R_x, p1)

#Interpolation vector in the rotated frame.
dp = p1-p0

print dp, "interp vec"

#To find the exact intersection location, we must first parameterize our interpolation line A(t) = p0 + dpt (pore frame).
#Then we can look at the projection of this line onto a circle perpendicualr to the pore's axis. 
#We then set the magnitude of this projection equal to the radius of our pore and solve for the free parameter t.
#The np.roots function requires our polynomial to be in standard form in order to solve for t. 
#I have separated out the expression in orders of t. 
const = p0[0]**2 + p0[1]**2 + y_pore**2 + x_pore**2 - 2*p0[0]*x_pore - 2*p0[1]*y_pore - R**2

first = 2*dp[0]*p0[0] + 2*dp[1]*p0[1] - 2*dp[0]*x_pore - 2*dp[1]*y_pore 

second = dp[0]**2 + dp[1]**2

coeffs = [second, first, const]

print coeffs, "coeffs"

roots = np.roots(coeffs)

t = roots[roots > 0]

#Now we can evaluate our interplation line at the appropriate value of t.
#This gives us the point of intersection in the pore frame.
p_intr = p0 + dp*t


theta = -1* theta 

R_x = np.array([[1,         0,                  0                   ],
                   [0,         np.cos(theta), np.sin(theta) ],
                   [0,         -np.sin(theta), np.cos(theta)  ]
                   ])

#Finally, we express the point of intersection in our lab frame by passively rotating back the way we came. 
p_intr = np.dot(R_x, p_intr)

print p_intr


#so now let's do that original shit

# d = np.linalg.norm(pos_intr - p0)

# dp = [p1[i] - p0[i] for i in range(3)]

# coeffs = [dp[0]**2 + dp[1]**2 + dp[2]**2, 2*(p0[0]*dp[0] + p0[1]*dp[1] + p0[2]*dp[2]), p0[0]**2 + p0[1]**2 + p0[2]**2 - d**2]

# roots = np.roots(coeffs)

# t = roots[roots > 0]
# t = t[0] #gives 

# print t























