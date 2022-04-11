#!/usr/bin/env python3
import time
from adafruit_motorkit import MotorKit
from ps3gamepad import gamepad


class MotorControl():
    def __init__(self):
        print("Init MotorControl")
        self.stop_flag = False
        self.kit = MotorKit()
        self.motors_off()


    def motors_off(self):
        # Set all the Motors to 'off'
        self.kit.motor1.throttle = 0
        self.kit.motor3.throttle = 0

    def set_motor_speed(self, lr_speeds):
        self.kit.motor1.throttle = lr_speeds[0]
        self.kit.motor3.throttle = lr_speeds[1]

    def stop_thread(self):
        self.stop_flag = True

    def runner(self):
        while not self.stop_flag:
            lr_speeds = self.calc_motor_speeds()
            #print("LeftMotor: " + str(lr_speeds[0]) +"\tRightMotor: " + str(lr_speeds[1]))
            self.set_motor_speed(lr_speeds)
            time.sleep(0.1)

        self.motors_off()
        print("Stopping MotorControl thread")

    def translate_range(self, value, src_low, src_high, dest_low, dest_high):
        """
        Translate the range of a given value from the scale of the source
        the scale of the destination. Parameters take floats
        """
        return (float(value - src_low) / (src_high - src_low)) * (dest_high - dest_low) + dest_low

    def scale_leftstick_x(self, value):
        """ Scales the left stick x axis, or ABS_X button """
        steering = self.translate_range(value,0, 255, -1, 1)
        return self.steering_deadzone_filter(steering)

    def scale_lr2(self, value):
        """ Scales the L2 / R2 buttons """
        return self.translate_range(value,0, 255, 0, 1)

    def steering_deadzone_filter(self, steering):
        deadzone = 0.05
        if(steering >= -deadzone and steering <= deadzone):
            steering = 0
        return steering

    def calc_motor_speeds(self):
        steering_direction = self.scale_leftstick_x(gamepad.btn_value['ABS_X'])
        forward_value = self.scale_lr2(gamepad.btn_value['ABS_RZ'])
        reverse_value = self.scale_lr2(gamepad.btn_value['ABS_Z'])

        # A value to help calculate motor speeds in different directions
        throttle_axis = 0
        if reverse_value > 0.1 and forward_value < 0.1:
            # move backwards
            throttle_axis = -reverse_value
        else:
            # move forwards
            throttle_axis = forward_value

        # LeftMotor
        left_motor_ratio = 1 + steering_direction
        if left_motor_ratio > 1.0:
            # stick right of center, maximum ratio 1.0
            left_motor_ratio = 1.0
        elif left_motor_ratio < 0.1:
            # turn in place, move left backwards
            left_motor_ratio = -1.0
        # Set left motor speed
        left_motor_speed = left_motor_ratio * throttle_axis

        # RightMotor
        right_motor_ratio = 1 - steering_direction
        if right_motor_ratio > 1:
            # stick left of center, maximum ratio 1.0
            right_motor_ratio = 1
        elif right_motor_ratio < 0.1:
            #turn in place, move right backwards
            right_motor_ratio = -1.0
        right_motor_speed = right_motor_ratio * throttle_axis

        left_motor_speed = self.motor_deadzone(left_motor_speed)
        right_motor_speed = self.motor_deadzone(right_motor_speed)
        return (left_motor_speed, right_motor_speed)

    # Set deadzone for motor speed
    def motor_deadzone(self, speed):
        deadzone = 0.25
        if speed > -deadzone and speed < deadzone:
            speed = 0
        return speed
