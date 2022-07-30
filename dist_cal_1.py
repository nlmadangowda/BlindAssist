import RPi.GPIO as GPIO
import time
import io
import sys
import os

GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER_L = 20
GPIO_ECHO_L = 21

GPIO_TRIGGER_R = 23
GPIO_ECHO_R = 24

RELAIS_1_GPIO = 12
#set GPIO direction (IN / OUT)
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)



def distance(trig,echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

while True:    
    L_dist = distance(GPIO_TRIGGER_L,GPIO_ECHO_L)
    R_dist = distance(GPIO_TRIGGER_R,GPIO_ECHO_R)

    print ("L= %.1f cm" % L_dist)
    print ("R= %.1f cm" % R_dist)

    time.sleep(1)