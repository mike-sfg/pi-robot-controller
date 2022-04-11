# pi-robot-controller

## Description
This is a collection of Python scripts for controlling a custom-built robot on Raspberry Pi. It allows the robot to be controlled by a wireless PS3 gamepad and also creates a video stream. The motor driver uses the `adafruit_motorkit` library and supports the [AdaFruit Motor Hat](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi). Since this code is robot-specific, it will probably need modification before it will work for your project. But if you find it helpful, feel free to use it.

## Pre-Requisites
Bluetooth connection to PS3 Gamepad setup so that `evdev` can recognize it.
AdaFruit motor hat setup and tested. `adafruit_motorkit` library installed.
Ensure Python packages used in the script are installed: evdev, picamera, socket, etc.

## Usage
1. Edit the file for your own robot-specific platform. You will need to pay special attention to the GPIO pins and comment-out or disable any portions of the code which aren't applicable for your robot. The pins specified below are using the Broadcom numbering system:
* 25 - PIR_PIN - a pin for a motion sensor. Set to input, but no action is presently taken when it changes. (declared in main.py)
* 23 - LEFT_LED - set for output (declared in led.py
* 24 - RIGHT_LED - set for output (declared in led.py)
3. Place files together in a folder. Execute main.py with python3.
4. Controls:
* Left Analog Stick - Left & Right steering
* R2 - Forward speed
* L2 - Reverse speed
* Triangle button - toggle LEDs
* Select button - Sentry mode (not yet implemented)
* Start button - Exit script
* D-Pad Left - Previous camera effect
* D-Pad Right - Next camera effect
5. Camera usage: This script uses the PiCamera library to stream video from the Raspberry Pi Camera Module V2. I have used the RPI Camera Viewer App on [Android](https://play.google.com/store/apps/details?id=ca.frozen.rpicameraviewer&gl=US) or [iOS](https://apps.apple.com/us/app/rpi-camera-viewer/id1312142156) to view the video streams. You can cycle through various camera effects, such as solarize, negative, or oil paint. I have found the cycling of effects to sometimes cause the video stream to crash, so this feature is experimental.



