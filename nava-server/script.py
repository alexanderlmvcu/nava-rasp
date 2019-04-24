#!/usr/bin/python
import RPi.GPIO as GPIO # Library for Raspberry Pi 
import time
import random
from random import randint

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.IN) 
GPIO.setup(3, GPIO.IN)

# Initializing variables that will be used to determine when the sensors have changed states from ON/OFF
S1 = GPIO.input(13)
S2 = GPIO.input(3)

tick = 0

Flag0 = False
Flag1 = True
FlagON = True
FlagDirection = True
FlagPosition = True
value = randint(5, 9)
print(value)

while True:

    while Flag0 == False: # Makes sure that Sensor 1 and Sensor2 are both zero 
        if S1 == 0 and S2 == 0: ## Flag becomes "True" so it exists the while loop, reads S1 and S2, and enters into the next loop
            Flag0 = True
            Flag1 = False
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
        else: # reads S1 and S2 until Flag0 becomes True
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)

    while Flag1 == False:
        if S1 == True and S2 == False:  # Sensor 1 is on and Sensor 2 is off 
            Flag1 = True  
            FlagON = False
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)

        if S1 == False and S2 == True:  # Sensor 1 is off and Sensor 2 is on
            Flag1 = True
            FlagON = False
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)

        else: # keeps reading until one sensor changes state
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
    
    # Forward direction loop
    while FlagON == False:
        if S1 == True and S2 == True: # Sensor 1 is on and Sensor 2 is on
            FlagON = True
            FlagDirection = False 
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
       
        else: # Keep reading until Sensor 1 is on and Sensor 2 is on
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
    
    # Direction Loop
    while FlagDirection == False:

        # FORWARD DIRECTION
        if S1 == False and S2 == True:  # Sensor 1 is off and Sensor 2 is on
            FlagDirection = True
            Flag0 = False
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
            tick += 1
            FlagPosition = False
            print("Forward")
            print(tick)
        
        # BACKWARD DIRECTION
        if S1 == True and S2 == False:
            FlagDirection = True
            Flag0 = False
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
            tick += -1
            FlagPosition = False
            print("Backward")
            print(tick)

        else: # Keep reading until the sense of direction is the same
            S1 = GPIO.input(13)
            S2 = GPIO.input(3)
    
    # #Determing the "sweet spot"
    while FlagPosition == False:
        if tick == 0:
            print("noise")
            FlagPosition = True

        if tick < value and tick > 0:
            print("Too low")
            FlagPosition = True

        if (tick > value):
            print("Too high")
            FlagPosition = True

        if tick == value:
            print("perfect")
            FlagPosition = True



