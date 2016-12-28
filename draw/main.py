
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

	v = rot_global_to_body(v)

	w perp to pv

	p is pen point
	o is origin

	x = p + k * w

	x = o + l * unit_x

	p + k * w = o + l * unit_x

	split above into x and y. then solve for k first

	

def set_motor_speed(s1, s2): pass

def set_tip_direction(v): pass



while true:
	# main loop
	
	# get time delta

	# calculate new position based on
	# time delta and previous motor speed

	# calculate new motor speeds

	# apply new notor speeds
	




