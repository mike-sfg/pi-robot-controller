#!/usr/bin/env python3
import evdev
import time
from led import lights
from camera_stream import cs


class PS3Gamepad():
    """ A class for a PS3 controller over Bluetooth."""

    def __init__(self):
        print("Finding ps3 controller...")
        ps3_controller = None
        while not ps3_controller:
            devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
            for device in devices:
                # Change device.name if your controller has a different name
                if device.name == 'Sony Computer Entertainment Wireless Controller':
                    ps3_controller = device.fn
                    print("Controller found!")
            if not ps3_controller:
                time.sleep(1)

        self.device = evdev.InputDevice(ps3_controller)

        # Initialize variables
        self.stop_flag = False

        # Dictionary of game controller buttons we want to monitor.
        self.btn_code = {'ABS_X': 0,  # Left-stick X axis
                     'ABS_Z': 2,  # L2 analog
                     'ABS_RZ': 5, # R2 analog
                     'BTN_SELECT': 314,
                     'BTN_START': 315,
                     'BTN_NORTH': 307,  # Triangle btn
                     'D-LEFT': 546, #D-Pad Left
                     'D-RIGHT': 547 #D-Pad Right
                     }
        print("Dictionary:")
        print(self.btn_code)

        # Dictionary of game buttons values we want to track.
        self.btn_value = {'ABS_X': 127,  # Left-stick X axis
                     'ABS_Z': 0,  # L2 analog
                     'ABS_RZ': 0, # R2 analog
                     'BTN_SELECT': 0,
                     'BTN_START': 0,
                     'BTN_NORTH': 0  # Triangle btn
                     }

    def runner(self):

        print("Gamepad Thread: starting")

        try:
            while not self.stop_flag:
                event = self.device.read_one()
                if event is None:
                    time.sleep(0.01)
                    continue
                elif event.type == 1:
                    if event.code == self.btn_code['BTN_START'] and event.value == 1:
                        print("Start Button is pressed, going to flag stop_flag")
                        self.stop_flag = True

                    # Select button pressed, enter sentry_mode
                    elif event.code == self.btn_code['BTN_SELECT'] and event.value == 1:
                            print("Select Button is pressed. ")

                    # Triangle button pressed, toggle LEDs
                    elif event.code == self.btn_code['BTN_NORTH'] and event.value == 1:
                            print("Triangle Button is pressed. ")
                            lights.toggle()

                    # Prev camera effect
                    elif event.code == self.btn_code['D-LEFT'] and event.value == 1:
                        cs.effect_prev()

                    # Next camera effect
                    elif event.code == self.btn_code['D-RIGHT'] and event.value == 1:
                        cs.effect_next()

                # Axis controls
                elif event.type == 3:
                    # Left stick, X axis
                    if event.code == self.btn_code['ABS_X']:
                        self.btn_value['ABS_X'] = event.value
                    # 'ABS_Z' ( L2 analog )
                    if event.code == self.btn_code['ABS_Z']:
                        self.btn_value['ABS_Z'] = event.value
                    # 'ABS_RZ' ( R2 analog )
                    if event.code == self.btn_code['ABS_RZ']:
                        self.btn_value['ABS_RZ'] = event.value

            print("Gamepad Thread: ending")

        except IOError as e:
            if e.errno == 11:
                pass

    def __del__(self):
        print("Closing Gamepad Device")
        self.device.close()


gamepad = PS3Gamepad()
