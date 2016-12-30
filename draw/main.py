
import numpy as np

# a - distnace between wheel centers
# b - distance from oeigin to pen
# c - distance from origin to rotation center

# the body origin is the center point between the wheels
# the robot position is given by the global ppsition of the
# origin and its orientation is an angle between the global
# and body axes

# the instantanwois rotation center is a point along a line
# that intersects both wheels
# in body coors, the instantaneous wheel center velocity is
# in the y direction
# 

def rot_global_to_body(v): pass

def calc_motor_speed(v):
	# v   global velocity of pen
	# w is perp to v
	# p is pen point
	# o is origin

	p = np.array([[0],[b]])

	v = rot_global_to_body(v)
	
	R = np.array([[0, -1],[1, 0]])

	w = R * v
	
	# x = p + k * w

	# x = o + l * unit_x

	# p + k * w = o + l * unit_x

	# split above into x and y. then solve for k first
	# y

	# p_1 + k * w[1] = 0
	# b + k * w_1 = 0
	
	k = -b / w[1]
	
	# x
	# x = p_0 + k * w_0
	x = k * w[0]
	
	# define a point for each wheel that lies on
	# the line perpendicular to the wheel axis
	# the distance and direction of the ppoint to its wheel
	# represents the speed and direction of the wheel
	# the intersection of the line and the wheel axis is the
	# point of rotation.
	# 
	# m = (s1 - s0) / a
	# y = m*(x-c)
	
	
	# r1 and r2 are distances from rotation center to wheel center
	
	r1 = -a/2.0 - c
	r2 = a/2.0 - c
	
	

def set_motor_speed(s1, s2): pass

def set_tip_direction(v): pass




sys.exit(0)

while true:
	# main loop
	
	# get time delta

	# calculate new position based on
	# time delta and previous motor speed

	# calculate new motor speeds

	# apply new notor speeds
	




