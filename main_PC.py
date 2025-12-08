import serial
import time

ser = serial.Serial("COM5", 115200)

current = None
start = time.time()
record = []

print("Enregistrement...")

while True:
    line = ser.readline().decode().strip()

    if line.startswith("ACTION="):
        action = line.split("=")[1]
        
        if action != current:
            if current is not None:
                duration = time.time() - start
                record.append((current, duration))
            
            current = action
            start = time.time()

    print(record)
