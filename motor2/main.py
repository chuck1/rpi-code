

import sys
import time
import RPi.GPIO as io


io.setmode(io.BCM)

in1_pin = 4
in2_pin = 17
in3_pin = 18

def set_motor(p, s):
	io.output(in3_pin, True)

	if s>0:
		io.output(in1_pin, True)
		io.output(in2_pin, False)
	if s<0:
		io.output(in1_pin, False)
		io.output(in2_pin, True)

	p.ChangeDutyCycle(abs(s))

def stop_motor():
	io.output(in3_pin, False)

io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(in3_pin, io.OUT)


p = io.PWM(in2_pin, 50)

p.start(20)

set_motor(p, 30)

time.sleep(1)

set_motor(p, -100)

time.sleep(1)

stop_motor()

p.stop()

io.output(in1_pin, False)
io.output(in2_pin, False)
io.output(in3_pin, False)

io.cleanup()

sys.exit(0)



def set(property, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()	
    except Exception as e:
        print("Error writing to: " + property + " value: " + value)
	print(e)
 
set("delayed", "0")
set("mode", "pwm")
set("frequency", "500")
set("active", "1")

def clockwise():
    io.output(in1_pin, True)    
    io.output(in2_pin, False)

def counter_clockwise():
    io.output(in1_pin, False)
    io.output(in2_pin, True)

clockwise()

while True:
    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
    direction = cmd[0]
    if direction == "f":
        clockwise()
    else: 
        counter_clockwise()
    speed = int(cmd[1]) * 11
    set("duty", str(speed))



