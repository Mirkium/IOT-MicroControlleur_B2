# ===== VOITURE ESP32 =====
from machine import Pin, PWM
import espnow
import network
import ujson

# --- Moteurs ---
RIGHT_F = Pin(13, Pin.OUT)
RIGHT_B = Pin(12, Pin.OUT)
ENA     = PWM(Pin(14), freq=1000)

LEFT_F  = Pin(26, Pin.OUT)
LEFT_B  = Pin(25, Pin.OUT)
ENB     = PWM(Pin(27), freq=1000)

speed = 800

def forward():
    RIGHT_F.on(); RIGHT_B.off()
    LEFT_F.on();  LEFT_B.off()
    ENA.duty(speed); ENB.duty(speed)

def backward():
    RIGHT_F.off(); RIGHT_B.on()
    LEFT_F.off();  LEFT_B.on()
    ENA.duty(speed); ENB.duty(speed)

def left():
    RIGHT_F.on(); RIGHT_B.off()
    LEFT_F.off(); LEFT_B.off()
    ENA.duty(speed); ENB.duty(0)

def right():
    RIGHT_F.off(); RIGHT_B.off()
    LEFT_F.on(); LEFT_B.off()
    ENA.duty(0); ENB.duty(speed)

def stop():
    RIGHT_F.off(); RIGHT_B.off()
    LEFT_F.off(); LEFT_B.off()
    ENA.duty(0); ENB.duty(0)

# --- ESP-NOW init ---
w0 = network.WLAN(network.STA_IF)
w0.active(True)

e = espnow.ESPNow()
e.active(True)

print("CAR READY")

while True:
    host, msg = e.recv()

    if not msg:
        continue

    cmd = msg.decode()

    # Commandes manuelles
    if cmd == "F":
        forward()
    elif cmd == "B":
        backward()
    elif cmd == "L":
        left()
    elif cmd == "R":
        right()
    elif cmd == "S":
        stop()

    # --- Mode autonome : réception d’un parcours ---
    elif cmd.startswith("P"):
        print("RECU PARCOURS")
        steps = ujson.loads(cmd[1:])
        print(steps)

        # Exécution du parcours
        for action, duration in steps:
            if action == "F":
                forward()
            elif action == "B":
                backward()
            elif action == "L":
                left()
            elif action == "R":
                right()
            else:
                stop()

            time.sleep_ms(duration)

        stop()
        print("PARCOURS TERMINE")
