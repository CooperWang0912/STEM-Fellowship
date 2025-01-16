import pygame  # Using pygame library's joystick functionality
import csv
import datetime

import os
import sys
os.environ["SDL_VIDEODRIVER"] = "dummy"

import board
import adafruit_lsm9ds1

import time

from digitalio import DigitalInOut, Direction
spi = board.SPI()
csag = DigitalInOut(board.D5)
csag.direction = Direction.OUTPUT
csag.value = True
csm = DigitalInOut(board.D6)
csm.direction = Direction.OUTPUT
csm.value = True
sensor = adafruit_lsm9ds1.LSM9DS1_SPI(spi, csag, csm)

from _XiaoRGEEK_SERVO_ import XR_Servo

servo = XR_Servo()
left_pulse = 30
right_pulse = 150
last_angle = 85


import RPi.GPIO
import time

max_throttle = 1
min_throttle = -1
max_pulse = 200
min_pulse = 0
zero_pulse = 100

GPIO = RPi.GPIO
GPIO.setmode(GPIO.BCM)

ENA = 13
ENB = 20
IN1 = 19
IN2 = 16
IN3 = 21
IN4 = 26
GPIO.setwarnings(False)

GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)

ENA_pwm=GPIO.PWM(ENA,1000)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(100)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(100)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
max_pulse = max_pulse
min_pulse = min_pulse
zero_pulse = zero_pulse
last_pulse = 100

def Motor_Forward():
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def Motor_Backward():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def Motor(pulse):
    if pulse >= 100:
        Motor_Forward()
        ENA_pwm.ChangeDutyCycle(pulse - 100)
        ENB_pwm.ChangeDutyCycle(pulse - 100)
    else:
        Motor_Backward()
        ENA_pwm.ChangeDutyCycle(100 - pulse)
        ENB_pwm.ChangeDutyCycle(100 - pulse)

def map_range(x, X_min, X_max, Y_min, Y_max):
    X_range = X_max - X_min
    Y_range = Y_max - Y_min
    y = Y_min + ((x - X_min) * Y_range / X_range)
    return int(y)

pygame.joystick.init()  # Initialize the joystick
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())] 

print(joysticks)

joysticks[0].init()

run = True

pygame.init()

data = []
collecting = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:  # If button is clicked
            if joysticks[0].get_button(3):  # If it is the stop button
                run = False  # Stop the program
                break
                pygame.quit()
            if joysticks[0].get_button(4):
               file_name = str(datetime.datetime.now())
               with open(file_name, mode = "w", newline = "", encoding = "utf-8") as file:
                   writer = csv.DictWriter(file, fieldnames = data[0].keys())
                   writer.writeheader()
                   writer.writerows(data)
                   data = []
            if event.type == pygame.QUIT:
                pygame.quit()
    if joysticks[0].get_axis(5) > 0:
        collecting = True
        label = int(joysticks[0].get_button(1))
        speed = -joysticks[0].get_axis(1)
        angle = joysticks[0].get_axis(2)
        accel_x, accel_y, accel_z = sensor.acceleration
        gyro_x, gyro_y, gyro_z = sensor.gyro
        row = {"label": label, "speed": speed, "angle": angle, "accel_x": accel_x, "accel_y": accel_y, "accel_z": accel_z, "gyro_x": gyro_x, "gyro_y": gyro_y, "gyro_z": gyro_z}
        data.append(row)
        if joysticks[0].get_axis(1) > 0:
            Motor(100 - map_range(joysticks[0].get_axis(1), 0, 1, 30, 100))
        elif joysticks[0].get_axis(1) < 0:
            Motor(300 - map_range(joysticks[0].get_axis(1), -1, 0, 130, 200))
        else: 
            Motor(zero_pulse)
        if joysticks[0].get_axis(2) != 0:
            servo.XiaoRGEEK_SetServoAngle(1, map_range(joysticks[0].get_axis(2), -1, 1, left_pulse, right_pulse))
        else:
            servo.XiaoRGEEK_SetServoAngle(1, last_angle)
    else:
        Motor(zero_pulse)
        servo.XiaoRGEEK_SetServoAngle(1, last_angle)
    time.sleep(1/60)

