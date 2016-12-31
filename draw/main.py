
import sys
import numpy as np
import time
import RPi.GPIO as io

io.setmode(io.BCM)

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

class Motor(object):
	def __init__(self, pin_onoff, pin_1, pin_2):
		self.pin_onoff = pin_onoff
		self.pin_1 = pin_1
		self.pin_2 = pin_2

		io.setup(pin_onoff, io.OUT)
		io.setup(pin_1, io.OUT)
		io.setup(pin_2, io.OUT)
	
		self.p = io.PWM(pin_1, 50)

		self.p.start(0)
	
	def set(self, s):
		io.output(self.pin_onoff, True)

		if s>0:
			io.output(self.pin_1, True)
			io.output(self.pin_2, False)
		if s<0:
			io.output(self.pin_1, False)
			io.output(self.pin_2, True)

		self.p.ChangeDutyCycle(abs(s))

	def stop(self):
		io.output(self.pin_onoff, False)



a = 1.0
b = 1.0

def rot_global_to_body(v):
	return v

def calc_motor_speed(v):
	# v   global velocity of pen
	# w is perp to v
	# p is pen point
	# o is origin

	p = np.array([[0],[b]])

	v = rot_global_to_body(v)
	
	R = np.array([[0, -1],[1, 0]])
	
	

	w = np.dot(R, v)
	
	print "p"
	print p
	print "v"
	print v
	print "R"
	print R
	print "w"
	print w

	# x = p + k * w

	# x = o + l * unit_x

	# p + k * w = o + l * unit_x

	# split above into x and y. then solve for k first
	# y

	# p_1 + k * w[1] = 0
	# b + k * w_1 = 0
	
	k = -b / w[1][0]

	
	# x
	# x = p_0 + k * w_0
	c = k * w[0][0]
	C = np.array([[c],[0]])
	
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

	R = p - C
	
	r1 = -a/2.0 - c
	r2 = a/2.0 - c
	
	rot = R[0][0] * v[1][0] - R[1][0] * v[0][0]

	s1 = rot * r1
	s2 = rot * r2

	print "a ",a
	print "b ",b
	print "k ",k
	print "c ",c
	print "r1",r1
	print "r2",r2
	print "R"
	print R
	print "rot",rot
	print "s1",s1
	print "s2",s2

	return (s1, s2)

def set_motor_speed(s1, s2):
	pass

def set_tip_direction(v):
	pass


#####

calc_motor_speed(np.array([[1],[1]]))

m1 = Motor(18, 4, 17)
m2 = Motor(2, 3, 15)

m1.set(50)
m2.set(50)

time.sleep(1)

m1.stop()
m2.stop()

io.cleanup()

sys.exit(0)

while true:
	# main loop
	
	# get time delta

	# calculate new position based on
	# time delta and previous motor speed

	# calculate new motor speeds

	# apply new notor speeds

	pass





