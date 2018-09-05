import serial
import time


ser = serial.Serial('COM3', 9600, timeout=0)
time.sleep(2) # waiting the screen loading
# var = input("Enter something: ")
var = "asedqedqw"
ser.write(var.encode())
