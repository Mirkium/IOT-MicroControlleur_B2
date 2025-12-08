from machine import Pin
import espnow
import network
import ujson
import time
from time import ticks_ms, ticks_diff

# -------- RECORDER --------
class Recorder:
    def __init__(self):
        self.steps = []
        self.recording = False
        self.lastAction = None
        self.startTime = None

    def start(self):
        print("REC START")
        self.recording = True
        self.steps = []
        self.lastAction = None
        self.startTime = ticks_ms()

    def stop(self):
        print("REC STOP")
        self.recording = False
        if self.lastAction is not None:
            duration = ticks_diff(ticks_ms(), self.startTime)
            self.steps.append((self.lastAction, duration))
        print("RECORDED STEPS:", self.steps)

    def update(self, action):
        if not self.recording:
            return

        if self.lastAction is None:
            self.lastAction = action
            self.startTime = ticks_ms()
            return

        if action != self.lastAction:
            now = ticks_ms()
            duration = ticks_diff(now, self.startTime)
            self.steps.append((self.lastAction, duration))
            self.lastAction = action
            self.startTime = now


# -------- BOUTONS --------
BTN_FORWARD  = Pin(13, Pin.IN, Pin.PULL_UP)
BTN_BACKWARD = Pin(12, Pin.IN, Pin.PULL_UP)
BTN_LEFT     = Pin(27, Pin.IN, Pin.PULL_UP)
BTN_RIGHT    = Pin(26, Pin.IN, Pin.PULL_UP)
BTN_AUTONOM  = Pin(14, Pin.IN, Pin.PULL_UP)  # deviendra bouton RECORD

# -------- ESP-NOW --------
w0 = network.WLAN(network.STA_IF)
w0.active(True)

e = espnow.ESPNow()
e.active(True)

CAR_MAC = b'\xAA\xBB\xCC\xDD\xEE\xFF'
e.add_peer(CAR_MAC)

def send(cmd):
    e.send(CAR_MAC, cmd)


# -------- REC ORDER SYSTEM --------
rec = Recorder()
record_mode = False


# -------- MAIN LOOP --------
while True:

    # Bouton 14 → toggle record start/stop
    if BTN_AUTONOM.value() == 0:
        if not record_mode:
            rec.start()
            record_mode = True
        else:
            rec.stop()
            send(b"P" + ujson.dumps(rec.steps))
            record_mode = False
        time.sleep_ms(300)   # anti-rebond

    # Lecture actions
    if BTN_FORWARD.value() == 0:
        action = b"F"
    elif BTN_BACKWARD.value() == 0:
        action = b"B"
    elif BTN_LEFT.value() == 0:
        action = b"L"
    elif BTN_RIGHT.value() == 0:
        action = b"R"
    else:
        action = b"S"

    # Envoi à la voiture
    send(action)

    # Enregistrement
    rec.update(action)

    time.sleep_ms(40)
