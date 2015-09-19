
import serial
import sys


def test(b):

	ser = serial.Serial('/dev/ttyAMA0', baudrate=b, timeout=3)

	ser.open()

	ser.write('AT\r\n')

	r = ser.readline()

	print 'baud',b
	print repr(r)

	ser.close()

baud = [9600, 57600, 115200]

for b in baud:
    test(b)

