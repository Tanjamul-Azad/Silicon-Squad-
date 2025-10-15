import time
import RPi.GPIO as GPIO

# === Pin map (BCM) ===
ENA, ENB = 12, 13       # PWM pins
IN1, IN2 = 5, 6         # Left side
IN3, IN4 = 20, 21       # Right side

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup
for p in [ENA, ENB, IN1, IN2, IN3, IN4]:
    GPIO.setup(p, GPIO.OUT)

# PWM setup
pwm_left = GPIO.PWM(ENA, 1000)   # 1 kHz PWM
pwm_right = GPIO.PWM(ENB, 1000)
pwm_left.start(0)
pwm_right.start(0)

# Helper: set motor speed (0–100)
def set_speed(left, right):
    """Change motor PWM speed safely"""
    left = max(0, min(100, left))
    right = max(0, min(100, right))
    pwm_left.ChangeDutyCycle(left)
    pwm_right.ChangeDutyCycle(right)

# --- Movement Functions ---

def stop():
    """Completely stop all motors and disable PWM outputs"""
    set_speed(0, 0)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)  # cut PWM signal
    GPIO.output(ENB, GPIO.LOW)
    time.sleep(0.2)
    print("🛑 Motors stopped (PWM + Direction off)")

def forward(speed=60):
    """Move both sides forward"""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed, speed)
    print(f"⬆️ Moving forward (speed={speed})")

def backward(speed=60):
    """Move both sides backward"""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed, speed)
    print(f"⬇️ Moving backward (speed={speed})")

def turn_left(speed=60):
    """Turn left (left backward, right forward)"""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed, speed)
    print("↩️ Turning left")

def turn_right(speed=60):
    """Turn right (left forward, right backward)"""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed, speed)
    print("↪️ Turning right")

def cleanup():
    """Safely stop everything and release GPIOs"""
    stop()
    pwm_left.stop()
    pwm_right.stop()
    GPIO.cleanup()
    print("🧹 GPIO cleaned up successfully")
