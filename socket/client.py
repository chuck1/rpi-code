import socket

#create an INET, STREAMing socket
s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect(("10.42.0.100", 9999))


while 1:
    print s.recv(128)


