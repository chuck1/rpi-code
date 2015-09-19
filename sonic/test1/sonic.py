
import wiringpi2
import time

wiringpi2.wiringPiSetupGpio()

TRIG = 23
ECHO = 24

print "Distance Measurement In Progress"

# Next, set your two GPIO ports as either inputs or outputs as defined previously.

wiringpi2.pinMode(TRIG,1)
wiringpi2.pinMode(ECHO,0)

# Then, ensure that the Trigger pin is set low, and give the sensor a second to settle.

wiringpi2.digitalWrite(TRIG, 0)

print "Waiting For Sensor To Settle"

time.sleep(2)

# The HC-SR04 sensor requires a short 10uS pulse to trigger the module,
# which will cause the sensor to start the ranging program
# (8 ultrasound bursts at 40 kHz) in order to obtain an echo response.
# So, to create our trigger pulse, we set out trigger pin high for 10uS then set it low again.

def measure():

	wiringpi2.digitalWrite(TRIG, 1)
	time.sleep(0.00001)
	wiringpi2.digitalWrite(TRIG, 0)

	pulse_start = time.time()
	while wiringpi2.digitalRead(ECHO)==0:
		pulse_start = time.time()
	
	# Once a signal is received, the value changes from low (0) to high (1),
	# and the signal will remain high for the duration of the echo pulse.
	# We therefore also need the last high timestamp for ECHO (pulse_end).

	pulse_end = time.time()      
	while wiringpi2.digitalRead(ECHO) == 1:
		pulse_end = time.time()      
	
	# We can now calculate the difference between the two recorded 
	# timestamps, and hence the duration of pulse (pulse_duration).

	pulse_duration = pulse_end - pulse_start
	
	distance = pulse_duration * 17150

	return distance

while True:
	
	distance = measure()
	
	distance = round(distance, 2)

	print "Distance:",distance,"cm"




wiringpi2.pinMode(TRIG,0)







