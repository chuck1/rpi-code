
import serial
import sys

b = sys.argv[1]
snd = sys.argv[2]

print 'baud',b
print 'send',repr(snd)

ser = serial.Serial('/dev/ttyAMA0', baudrate=b, timeout=3)

ser.open()

ser.write(snd + '\r\n')

r = ser.readline()

print repr(r)

ser.close()


