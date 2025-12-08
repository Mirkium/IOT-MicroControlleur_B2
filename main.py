import uasyncio as asyncio
from car import MotorManager, leftMotor, rightMotor
from command import Command
from recordTraject import Recorder

async def commandLoop(cmd, manager):
    """Boucle qui lit les boutons toutes les 20 ms."""
    while True:
        action = cmd.read()

        if action == "autonom":
            print("Mode autonome activé !")

        elif action:  
            manager.doAction(action)
        else:
            cmd.stopIfNoKey()

        await asyncio.sleep_ms(20)


async def main():
    manager = MotorManager(leftMotor, rightMotor)
    cmd = Command(manager)
    recorder = Recorder(manager)

    # Lancement de la boucle d’enregistrement
    asyncio.create_task(recorder.recordLoop())

    # Exemple : on démarre l'enregistrement ici
    recorder.startRecord()

    # Lancement de la lecture des commandes
    await commandLoop(cmd, manager)


asyncio.run(main())
