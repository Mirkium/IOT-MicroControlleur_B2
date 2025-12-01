from time import ticks_ms, ticks_diff
from car import MotorManager
import uasyncio as asyncio

class Recorder:
    def __init__(self, manager):
        self.manager = manager
        self.recordSteps = []
        self.recording = False
        self.currentAction = None
        self.actionStart = None

    def startRecord(self):
        print("Recording started")
        self.recording = True
        self.actionStart = ticks_ms()
        self.currentAction = self.manager.lastAction

    def stopRecord(self):
        print("Recording stopped")
        self.recording = False

    async def recordLoop(self):
        while True:
            if self.recording:
                # Nouvelle action détectée ?
                if self.manager.lastAction != self.currentAction:
                    # Fin de l’action précédente
                    end = ticks_ms()
                    duration = ticks_diff(end, self.actionStart)

                    # Enregistrer le step
                    action, speed = self.currentAction
                    self.recordSteps.append({
                        "action": action,
                        "speed": speed,
                        "durationMS": duration
                    })

                    # Nouvelle action
                    self.currentAction = self.manager.lastAction
                    self.actionStart = ticks_ms()

            await asyncio.sleep_ms(10)
