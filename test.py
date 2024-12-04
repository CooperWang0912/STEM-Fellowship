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
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
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

def Motor_TurnLeft():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def Motor_TurnRight():
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def Motor_Stop():
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)

def Motor(pulse):
    if pulse >= 100:
        Motor_Forward()
        ENA_pwm.ChangeDutyCycle(pulse - 100)
        ENB_pwm.ChangeDutyCycle(pulse - 100)
    else:
        Motor_Backward()
        ENA_pwm.ChangeDutyCycle(100 - pulse)
        ENB_pwm.ChangeDutyCycle(100 - pulse)

Motor(zero_pulse+20)
time.sleep(2)
Motor(zero_pulse)