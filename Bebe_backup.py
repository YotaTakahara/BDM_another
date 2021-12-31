#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from pydub import AudioSegment
from pydub.playback import play

TRIG = 16
ECHO = 18
NOMICIR=0

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
        dis = distance()
        if 10<dis and dis<1000:
            count+=1
        else:
            count=0
        if count>0:
            che
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def checkCall():
    print("call start")
    sound = AudioSegment.from_mp3("sakekas.mp3")
    play(sound)
    time.sleep(1.0)

def loop():
    count=0
    while True:
        dis = distance()
        if 10<dis and dis<1000:
            count+=1
        else:
            count=0
        if count>3:
            checkCall()
            count=0
        print ('Distance: %.2f' % dis)
        time.sleep(0.3)

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()