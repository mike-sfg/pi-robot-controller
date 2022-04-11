#!/usr/bin/env python3
import time
import threading
import RPi.GPIO as GPIO
from subprocess import call
from ps3gamepad import gamepad
from led import lights
from motorcontrol import MotorControl
from camera_stream import cs


if __name__ == "__main__":
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # PIR Pin numbers
    PIR_PIN = 25
    GPIO.setup(PIR_PIN, GPIO.IN)    

    # Threads
    gamepad_thread = threading.Thread(target=gamepad.runner)
    gamepad_thread.start()
    print("Wait for thread to finish")

    mc = MotorControl()
    mc_t = threading.Thread(target=mc.runner)

    # Camera stream thread
    cs_t = threading.Thread(target=cs.runner)
    
    mc_t.start()
    cs_t.start()

    # Wait for gamepad thread to end
    gamepad_thread.join()

    # End motorcontrol thread
    mc.stop_thread()
    mc_t.join()
    # End camera stream thread
    cs.terminate()
    cs_t.join()

    # Cleanup
    GPIO.cleanup()
    print("Finished, going to exit now")
    # Uncomment next line to shutdown OS on exit
    #call("sudo shutdown -P now", shell=True)
    exit()
