#!/usr/bin/env python3
import RPi.GPIO as GPIO

# LED GPIO Pin numbers
LEFT_LED = 23
RIGHT_LED = 24

class Led():
    def __init__(self):
        print("init Led")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(LEFT_LED,GPIO.OUT)
        GPIO.setup(RIGHT_LED,GPIO.OUT)
        # Other properties for future use
        #self.left_led_on = False
        #self.right_led_on = False
        self.lightsOn = False
        #self.alternate = False
        #Set off initially
        GPIO.output(LEFT_LED,GPIO.LOW)
        GPIO.output(RIGHT_LED,GPIO.LOW)

    def toggle(self):
        if self.lightsOn:
            #LEDs are on, toggle off
            GPIO.output(LEFT_LED,GPIO.LOW)
            GPIO.output(RIGHT_LED,GPIO.LOW)
            self.lightsOn = False
        else:
            # Turn on LEDs
            print("Toggle on")
            GPIO.output(LEFT_LED,GPIO.HIGH)
            GPIO.output(RIGHT_LED,GPIO.HIGH)
            self.lightsOn = True

    def __del__(self):
        # Cleanup GPIO pins in use by this class    
        # If GPIO.cleanup() called elsewhere, then board numbering will be None
        if (GPIO.getmode() != None):
            print("GPIO Mode: " + str(GPIO.getmode()))
            GPIO.cleanup((LEFT_LED, RIGHT_LED))

lights = Led()
