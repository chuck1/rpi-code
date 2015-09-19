
import wiringpi2

wiringpi2.wiringPiSetupGpio()

TRIG = 23
ECHO = 24

wiringpi2.pinMode(TRIG,0)
wiringpi2.pinMode(ECHO,0)


