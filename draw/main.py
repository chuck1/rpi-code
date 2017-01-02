
import sys
import numpy as np
import time
import json
import math

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

def rotmat(a):
	c = math.cos(a)
	s = math.sin(a)
		
	R = np.array([[c, -s],[s, c]])
	
	return R

class Robot(object):
	def __init__(self, m1, m2):
		self.m1 = m1
		self.m2 = m2

		self.position = np.array([[0],[0]])
		self.orientation = 0.0

		self.s1 = 0
		self.s2 = 0

		# must be calibrated
		# the linear speed of the wheel center in m/s equal to 100% motor speed
		self.C1 = 0.05
		self.C2 = 0.05
		
		
		self.wheel_speed = 25.0
		
	def draw(self, image):
		self.image = image

	def run(self):
	
		t00 = time.time()
		t0 = t00

		# test values
		self.calc_motor_speed(np.array([[1],[1]]))
	
		while True:
			# calc delta time
			t1 = time.time()
			dt = t1 - t0
			t0 = t1

			self.update_position(dt)
			
			print "p [{:16.2f},{:16.2f}] a {:16.2f}".format(self.position[0][0], self.position[1][0], self.orientation)
			
			if (t1 - t00) > 1.0:
				break

		self.m1.stop()
		self.m2.stop()

	def set_motor_speed(self):
		self.m1.set(self.s1)
		self.m2.set(self.s2)

	def update_position(self, dt):
		# based on current motor speeds and time passed
		# estimate new position of robot
	
		# O - center of rotation (global)
		
		C1 = self.rot_body_to_global(self.C)

		O = self.position - C1
	
		# change in angle
		angle = self.omega * dt
		
		R = rotmat(angle)
		
		C2 = np.dot(R, C1)

		self.position = O + C2
		
		self.orientation += angle

		print "C1"
		print C1
		print "C2"
		print C2
		print "O"
		print O

	def calc_wheel_center_speed(self):

		self.ws1 = self.s1 * self.C1
		self.ws2 = self.s2 * self.C2
	
		self.omega = self.r1 * self.ws1

	def rot_global_to_body(self, v):
		a = -self.orientation
		R = rotmat(a)		
		return np.dot(R, v)
	
	def rot_body_to_global(self, v):
		a = self.orientation
		R = rotmat(a)		
		return np.dot(R, v)
	
	def calc_motor_speed(self, v):
		# v   global velocity of pen
		# w is perp to v
		# p is pen point
		# o is origin
	
		p = np.array([[0],[b]])
	
		v = self.rot_global_to_body(v)
		
		R = np.array([[0, -1],[1, 0]])
		
		w = np.dot(R, v)
	
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
		C = np.array([[-c],[0]])
		
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
	
		R = p - (-C)
		
		r1 = -a/2.0 - c
		r2 = a/2.0 - c
		
		rot = R[0][0] * v[1][0] - R[1][0] * v[0][0]
	
		s1 = rot * r1
		s2 = rot * r2
	
		print "p"
		print p
		print "v"
		print v
		print "R"
		print R
		print "w"
		print w
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
		
		s_max = max(abs(s1), abs(s2))
		print "s_max", s_max	
		
		s1 = s1 / s_max * self.wheel_speed
		s2 = s2 / s_max * self.wheel_speed
	
		print "s1",s1
		print "s2",s2
	
		self.c = c
		self.C = C
		self.r1 = r1

		self.s1 = s1
		self.s2 = s2

		self.calc_wheel_center_speed()

		self.set_motor_speed()

		return (s1, s2)

class Motor(object):
	def __init__(self, pin_onoff, pin_1, pin_2, f):
		self.pin_onoff = pin_onoff
		self.pin_1 = pin_1
		self.pin_2 = pin_2

		io.setup(pin_onoff, io.OUT)
		io.setup(pin_1, io.OUT)
		io.setup(pin_2, io.OUT)
	
		self.p = io.PWM(pin_1, f)

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



def set_motor_speed(s1, s2):
	pass

def set_tip_direction(v):
	pass


###############################

def sample_image():
	with open("image1.txt", "r") as f:
		img = json.loads(f.read())

	return img

def motor_test(m1, m2):
	m1.set(100)
	m2.set(5)

	time.sleep(5)

	m1.stop()
	m2.stop()


img = sample_image()

print img

m1 = Motor(18, 4, 17, 10)
m2 = Motor( 2, 3, 15, 10)

robot = Robot(m1, m2)

robot.calc_motor_speed(np.array([[1],[1]]))

robot.run()

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





