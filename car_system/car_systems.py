#coding:utf-8
import serial
import time

ser1 = serial.Serial('/dev/ttyACM0',115200)

def connect():
    ser1 = serial.Serial('/dev/ttyACM0',115200)
    
def go_Advance():
    ser1.write('i'.encode('utf-8'))

def go_Left():
    ser1.write('j'.encode('utf-8'))

def go_Right():
    ser1.write('l'.encode('utf-8'))

def go_Back():
    ser1.write('k'.encode('utf-8'))

def stop_Stop():
    ser1.write('m'.encode('utf-8'))

def avoid(times):
    for i in range(times):
        ser1.write('A'.encode('utf-8'))
        time.sleep(0.5)

def right():
    ser1.write('s'.encode('utf-8'))

def left():
    ser1.write('a'.encode('utf-8'))
                          
def close():
    ser1.close()
    ser1 = serial.Serial()

