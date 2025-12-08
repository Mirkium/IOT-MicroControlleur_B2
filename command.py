from machine import Pin
from car import defaultSpeed

class Command:
    def __init__(self, manager):
        self.manager = manager

        self.btn_forward   = Pin(13, Pin.IN, Pin.PULL_UP)
        self.btn_backward  = Pin(12, Pin.IN, Pin.PULL_UP)
        self.btn_left      = Pin(27, Pin.IN, Pin.PULL_UP)
        self.btn_right     = Pin(26, Pin.IN, Pin.PULL_UP)
        self.btn_autonom   = Pin(14, Pin.IN, Pin.PULL_UP)

    def read(self):
        """
        Lit les boutons et appelle MotorManager si une action est demandée.
        Retourne True si une action a été effectuée.
        """
        if self.btn_forward.value() == 0:
            self.manager.forward(defaultSpeed)
            return True
        
        if self.btn_backward.value() == 0:
            self.manager.backward(defaultSpeed)
            return True
        
        if self.btn_left.value() == 0:
            self.manager.turnLeft_Forward(defaultSpeed)
            return True
        
        if self.btn_right.value() == 0:
            self.manager.turnRight_Forward(defaultSpeed)
            return True
        
        if self.btn_autonom.value() == 0:
            return "autonom"

        return False

    def stopIfNoKey(self):
        """Arrête le robot si aucun bouton n'est pressé."""
        if (self.btn_forward.value() == 1 and
            self.btn_backward.value() == 1 and
            self.btn_left.value() == 1 and
            self.btn_right.value() == 1):
            self.manager.stop()
