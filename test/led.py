#coding:utf-8

import serial
import time

ser = serial.Serial('/dev/ttyACM1',9600)


for i in range(10):
    # red
    ser.write('1'.encode('utf-8'))
    time.sleep(2)
    # green
    ser.write('2'.encode('utf-8'))
    time.sleep(2)
    # blue
    ser.write('3'.encode('utf-8'))
    time.sleep(2)

ser.write('0'.encode('utf-8'))

ser.close()
