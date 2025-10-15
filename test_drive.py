import RPi.GPIO as GPIO
import time

# BCM pin numbers
ENA, ENB = 12, 13       # PWM pins
IN1, IN2 = 5, 6          # Left side
IN3, IN4 = 20, 21        # Right side

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set all pins as output
for p in [ENA, ENB, IN1, IN2, IN3, IN4]:
    GPIO.setup(p, GPIO.OUT)

# Start PWM
pwm_left = GPIO.PWM(ENA, 1000)
pwm_right = GPIO.PWM(ENB, 1000)
pwm_left.start(0)
pwm_right.start(0)

def set_speed(left, right):
    pwm_left.ChangeDutyCycle(left)
    pwm_right.ChangeDutyCycle(right)

def stop():
    set_speed(0, 0)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    print("🛑 Stopped")

def forward(speed=60, duration=3):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed, speed)
    print(f"⬆️ Moving FORWARD for {duration}s at speed={speed}")
    time.sleep(duration)
    stop()

def backward(speed=60, duration=3):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed, speed)
    print(f"⬇️ Moving BACKWARD for {duration}s at speed={speed}")
    time.sleep(duration)
    stop()

try:
    print("🚗 4-wheel test started")
    forward(60, 3)
    time.sleep(1)
    backward(60, 3)
    print("✅ Test complete")

finally:
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
