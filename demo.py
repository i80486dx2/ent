import sys
sys.path.append('talk')
import subprocess
import socket
import re
import jtalk
import gcp_talk
import os
import string
import random
import numpy as np
from numpy.random import *
import time
import serial
import schedule
import threading
import pya3rt

ser = serial.Serial('/dev/ttyACM1',9600)
time.sleep(2)
# red   1
# green 2
# blue  3 
ser.write('2'.encode('utf-8'))

while True:
    a = int(input())
    # greet
    if a == 1:
        ser.write('3'.encode('utf-8'))
        jtalk.jtalk("おはようございます")

    # say yourname
    if a == 2:
        ser.write('3'.encode('utf-8'))
        jtalk.jtalk("エントと申します。よろしくお願いします。")

    # samuine
    if a == 3:
        ser.write('3'.encode('utf-8'))
        jtalk.jtalk("今日は寒いね。")
        jtalk.jtalk("会津若松はまだ雪が残っているよ。")

    if a == 4:
        ser.write('3'.encode('utf-8'))
        jtalk.jtalk("喉が乾いたよ")

        
    if a == 5:
        ser.write('3'.encode('utf-8'))
        jtalk.jtalk("さようなら、人類。")

    ser.write('2'.encode('utf-8'))
        
        
