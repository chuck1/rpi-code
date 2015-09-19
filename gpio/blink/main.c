
#include <unistd.h>
#include <wiringPi.h>

int pin = 14;

int main()
{
	wiringPiSetupGpio();
	
	pinMode(pin, OUTPUT);

	while(1) {
		digitalWrite(pin, HIGH);
		sleep(1);
		digitalWrite(pin, LOW);
		sleep(1);
	}
}

