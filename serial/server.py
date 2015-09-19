
import serial
import wiringpi2

import re


def send(ser, m):
	ser.write(m+'\r\r\n')

def clear(ser):
	while(True):
		rcv = ser.readline()
		if rcv == 'OK\r\n':
			break;
		if rcv == 'ERROR\r\n':
			print 'ERROR'
			break;

def read(ser):
	while(True):
		rcv = ser.readline()
		
		m = re.match('\+IPD,(\d+),(\d+):(.*)', rcv)

		if m:
			l = int(m.group(2))
			msg = m.group(3)[:l]

			print msg

			if msg == '17,HIGH':
				wiringpi2.digitalWrite(17,1)
			elif msg == '17,LOW':
				wiringpi2.digitalWrite(17,0)


wiringpi2.wiringPiSetupGpio()
wiringpi2.pinMode(17,1)

ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1)
ser.open()

send(ser, 'AT+CIPMUX=1')
clear(ser)
send(ser, 'AT+CIPSERVER=1,9999')
clear(ser)

read(ser)

