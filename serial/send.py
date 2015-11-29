
import serial
import sys

snd = sys.argv[1]

print 'send',repr(snd)

ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=3)

ser.open()

ser.write(snd + '\r\n')

r = ser.readline()

print repr(r)

ser.close()


