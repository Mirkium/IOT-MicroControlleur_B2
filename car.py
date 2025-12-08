from time import sleep
from machine import Pin, PWM, time_pulse_us
import uasyncio as asyncio

# ============== PIN CONFIGURATION =================

TRIG_PIN   = 4
ECHO_PIN   = 16

MOTOR_RIGHT_FORWARD  = 13
MOTOR_RIGHT_BACKWARD = 12
ENA        = 14

MOTOR_LEFT_FORWARD   = 26
MOTOR_LEFT_BACKWARD  = 25
ENB        = 27

defaultSpeed = 800  # vitesse d'avance (512 à 1023)

# ============== HARDWARE INITIALISATION ==============

# Motor right pins
inRight_Forward = Pin(MOTOR_RIGHT_FORWARD, Pin.OUT)
inRight_Backward = Pin(MOTOR_RIGHT_BACKWARD, Pin.OUT)
ena = PWM(Pin(ENA), freq=1000)

# Motor left pins
inLeft_Forward = Pin(MOTOR_LEFT_FORWARD, Pin.OUT)
inLeft_Backward = Pin(MOTOR_LEFT_BACKWARD, Pin.OUT)
enb = PWM(Pin(ENB), freq=1000)

# Ultrasonic sensor pins
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# ==================== CLASSES =====================

class Motor:
    def __init__(self, PIN_FORWARD, PIN_BACKWARD, PWM_CHANNEL, speed=0):
        self.forward = PIN_FORWARD
        self.backward = PIN_BACKWARD
        self.en = PWM_CHANNEL
        self.speed = speed

    def move(self, speed):
        if speed is None:
            return
        
        self.speed = speed

        if speed < 512:
            self.moveBackward()
        else:
            self.moveForward()

    def moveForward(self):
        self.forward.value(1)
        self.backward.value(0)
        pwm_value = self.speed - 512
        if pwm_value < 0: pwm_value = 0
        self.en.duty(pwm_value)
        

    def moveBackward(self):
        self.forward.value(0)
        self.backward.value(1)
        pwm_value = 512 - self.speed
        if pwm_value < 0: pwm_value = 0
        self.en.duty(pwm_value)       

    def stop(self):
        self.forward.value(0)
        self.backward.value(0)
        self.en.duty(0)
        self.speed = 0


class MotorManager:
    def __init__(self, leftMotor, rightMotor):
        self.left = leftMotor
        self.right = rightMotor
        self.running = False
        self.lastAction = None

    def forward(self, speed=defaultSpeed):
        self.lastAction = ("forward", speed)
        print("Robot move forward")
        self.right.move(speed)
        self.left.move(speed)
        return True
        
    def backward(self, speed=defaultSpeed):
        self.lastAction = ("backward", speed)
        print("Robot move backward")
        self.right.move(-speed)
        self.left.move(-speed)
        return True
        
    def turnLeft_Forward(self, speed=defaultSpeed):
        self.lastAction = ("left", speed)
        print("Robot turn left")
        self.right.move(speed)
        self.left.stop()
        return True
        
    def turnRight_Forward(self, speed=defaultSpeed):
        self.lastAction = ("right", speed)
        print("Robot turn right")
        self.right.stop()
        self.left.move(speed)
        return True
    
    def turnLeft_Backward(self, speed=defaultSpeed):
        self.lastAction = ("left_backward", speed)
        self.right.stop()
        self.left.move(-speed)
        return True
    
    def turnRight_Backward(self, speed=defaultSpeed):
        self.lastAction = ("right_backward", speed)
        self.right.move(-speed)
        self.left.stop()
        return True    
        
    def stop(self):
        self.lastAction = ("stop", 0)
        print("Robot stopped")
        self.left.stop()
        self.right.stop()
        
    def start(self, speed=defaultSpeed):
        self.running = True
        self.forward(speed)

    def pause(self):
        print("MotorManager: PAUSED")
        self.running = False
        self.stop()

    def resume(self):
        print("MotorManager: RESUMED")
        self.running = True
        lastAction, speed = self.lastAction
        self.apply(lastAction, speed)

    def apply(self, action, speed):
        """Ré-exécute une action depuis son nom."""
        if action == "forward": self.forward(speed)
        elif action == "backward": self.backward(speed)
        elif action == "left": self.turnLeft_Forward(speed)
        elif action == "right": self.turnRight_Forward(speed)
        elif action == "stop": self.stop()



# ================== SENSOR FUNCTIONS ==================

def getSensorDistance():
    # send trigger pulse
    trig.off()
    sleep(0.002)
    trig.on()
    sleep(0.00001)
    trig.off()

    try:
        duration = time_pulse_us(echo, 1, 30000)
        distance_cm = (duration / 2) / 29.1
        return distance_cm
    except OSError:
        return 0


# ================ ASYNC SENSOR TASK =================

async def manageSensor(manager):
    print("Sensor loop started...")
    while True:
        distance = getSensorDistance()

        if distance < 15 and manager.running:
            print("Obstacle detected at:", distance, "cm")
            manager.pause()

        if distance >= 15 and not manager.running:
            print("Obstacle cleared at:", distance, "cm")
            manager.resume()

        await asyncio.sleep_ms(50)


# ================ MAIN ASYNC PROGRAM ================

async def main():
    manager = MotorManager(leftMotor, rightMotor)

    # Start robot immediately
    manager.start(defaultSpeed)

    # Run sensor task in parallel
    await manageSensor(manager)


# =================== RUN =====================

rightMotor = Motor(inRight_Forward, inRight_Backward, ena)
leftMotor  = Motor(inLeft_Forward, inLeft_Backward, enb)

asyncio.run(main())
