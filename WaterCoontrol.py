
import pygame
import RPi.GPIO as GPIO
import time
import os
import sys
import subprocess

# Set up pins
MotorPin1   = 17
MotorPin2   = 27
MotorEnable = 22
TRIG = 23
ECHO = 24
NOMICIR=0
directions = {'CW': 1, 'CCW': -1, 'STOP': 0}


global_average=4
global_count=0
global_array=[]
global_definition=5
global_definition_array=["music/nomi.mp3","music/badopa.mp3","music/ippanppi-po-.mp3","music/haibokusha.mp3"]





def setup():
	# Set the GPIO modes to BCM Numbering
	GPIO.setmode(GPIO.BCM)
	# Set pins to output
	GPIO.setup(MotorPin1, GPIO.OUT)
	GPIO.setup(MotorPin2, GPIO.OUT)
	GPIO.setup(MotorEnable, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)



# Define a motor function to spin the motor
# direction should be 
# 1(clockwise), 0(stop), -1(counterclockwise)
def motor(direction):
	# Clockwise
	if direction == 1:
		# Set direction
		GPIO.output(MotorPin1, GPIO.HIGH)
		GPIO.output(MotorPin2, GPIO.LOW)
		# Enable the motor
		GPIO.output(MotorEnable, GPIO.HIGH)
		print ("Clockwise")
	# Counterclockwise
	if direction == -1:
		# Set direction
		GPIO.output(MotorPin1, GPIO.LOW)
		GPIO.output(MotorPin2, GPIO.HIGH)
		# Enable the motor
		GPIO.output(MotorEnable, GPIO.HIGH)
		print ("Counterclockwise")
	# Stop
	if direction == 0:
		# Disable the motor
		GPIO.output(MotorEnable, GPIO.LOW)
		print ("Stop")

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def checkCall():
	print("call start")
	ans_count=0	
	
    # p=os.system("sudo mplayer -xy 1900 -geometry 50%:50% music/grandBlue1.mov")
    # p1=os.system("sudo mplayer -xy 1900 -geometry 50%:50% music/grandBlue2.mov")
	while True:
		pygame.mixer.init()
		pygame.mixer.music.load("music/callStart.mp3")
		pygame.mixer.music.play(1)
		countforCall=0
		while countforCall<2:
			
			dis =distance()
			ans_count+=1
            
			if dis<=10 or 1000<=dis:#if there is a cup,call stops.
                
				print("call stops suddenly")
				return ans_count		
			time.sleep(0.5)
			countforCall+=1
        			
        # if dis<=10 or 1000<=dis:#if there is a cup,call stops.
        #     return ans_count		
        
    # pygame.mixer.music.stop()
 #   time.sleep(10.0)



def pour_sake():
	global global_definition
	print("global_definition: "+str(global_definition))
	motor(directions['CW'])
	if global_definition==0:
		time.sleep(12)
	elif global_definition==1:	
		time.sleep(10)
	elif global_definition==2:
		time.sleep(7)
	elif global_definition==3:
		time.sleep(3)
	else:
		time.sleep(5)
	motor(directions['STOP'])

def change_action():
	global global_definition
	global global_array
	global global_average
	sub_num=int(global_average/2)
	ans=sum(global_array)/len(global_array)
	for i in range(len(global_array)-sub_num):
		global_array.pop(0)
	#ans=sum(global_array)/global_average
	print("ans: "+str(ans))
	change_action_execute(ans)

def change_action_execute(ans):
	global global_definition
	if  ans<7:
		global_definition=0
	elif 7<=ans and ans <10:
		global_definition=1    
	elif 10<=ans and ans<=30:
		global_definition=2
	else :
		global_definition=3
	pygame.mixer.init()
	pygame.mixer.music.load(global_definition_array[global_definition])
	pygame.mixer.music.play(1)	
  
  

def nomisa_definition(tmpX):
	global global_count
	global global_array
    
	if global_count<global_average:
		global_array.append(tmpX)
        
	else:
		change_action()
		global_count=0
	print("global_array:"+str(global_array))	

def main():
	count=0
	global global_count

	# Define a dictionary to make the script more readable
	# CW as clockwise, CCW as counterclockwise, STOP as stop
	# directions = {'CW': 1, 'CCW': -1, 'STOP': 0}
	pouring_is_needed = True
	while True:
		
		# Clockwise
		#time.sleep(5)
		#time.sleep(5)
		# Stop
		#if 10<dis and dis<1000:
		motor(directions['STOP'])
		#time.sleep(5)
	

		dis = distance()
		if 10<dis and dis<1000:#A cup does not exist
			count+=1
		else:# A cup exists
			count=0
			if pouring_is_needed==True:
				pour_sake()
				pouring_is_needed=False
		if count>1:
			pouring_is_needed=True
			tmpX=checkCall()
			global_count+=1
			print("global_count: "+str(global_count))
			nomisa_definition(tmpX)
			count=0
		print('Distance: %.2f' % dis)
		time.sleep(0.3)


def destroy():
	# Stop the motor
	GPIO.output(MotorEnable, GPIO.LOW)
	# Release resource
	GPIO.cleanup()    

# If run this script directly, do:
if __name__ == '__main__':
	setup()
	try:
		main()
	# When 'Ctrl+C' is pressed, the program 
	# destroy() will be executed.
	except KeyboardInterrupt:
		destroy()
