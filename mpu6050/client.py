import socket
import struct
import numpy as np
import pylab as pl

#create an INET, STREAMing socket
s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect(("10.42.0.100", 9999))

def read():
    d = s.recv(128)
    data = struct.unpack('iiiiiid',d)
    a = np.array([data[:3]]) / float(0x7fff)
    g = np.array([data[3:]]) / float(0x7fff)
    t = np.array([[data[6]]])
    return a,g,t

T = np.zeros((0,1))
A = np.zeros((0,3))
G = np.zeros((0,3))

A_cal = np.zeros((1,3))
  

try:

    print "calibrating"
    for i in range(100):
        a,g,_ = read()
        A_cal += a
    A_cal /= 100.
    
    print "done", A_cal
    

    i = 0
    
    while 1:
        i += 1
        a,g,t = read()

        #print np.shape(A)
        #print i

        a -= A_cal

        A  = np.concatenate((A,a),axis=0)
        
        T = np.concatenate((T,t),axis=0)
        #print a,g

except (KeyboardInterrupt, SystemExit):
    pass

print "exiting"

print T[0]

# shift time
T -= T[0,0]

n = np.shape(A)[0]
I = range(n)

V = np.zeros((n,3))
X = np.zeros((n,3))

for i in range(1,n):
    V[i] = V[i-1] + A[i-1] * (T[i] - T[i-1])
    X[i] = X[i-1] + V[i-1] * (T[i] - T[i-1])


print "avg", np.average(A)

pl.figure()
pl.plot(I,A[:,0])

pl.figure()
pl.plot(I,V[:,0])

pl.figure()
pl.plot(I,X[:,0])

pl.figure()
pl.plot(I,T[:,0])

pl.show()








