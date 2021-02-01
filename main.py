import sys
sys.path.append('talk')
sys.path.append('car_system')
import subprocess
import socket
import re
import jtalk
import gcp_talk
import car_systems
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

# uses result_end_time currently only avaialble in v1p1beta, will be in v1 soon
from google.cloud import speech
import pyaudio
from six.moves import queue

from datetime import datetime

# sensor variable
temp = 0
humi = 0

# Fabo LED
ser = serial.Serial('/dev/ttyACM1',9600)
time.sleep(2)
# red   1
# green 2
# blue  3 
ser.write('2'.encode('utf-8'))
time.sleep(1)

# function area
def initialize():
    ser.write('0'.encode('utf-8'))
    time.sleep(0.5)
    ser.write('2'.encode('utf-8'))
    time.sleep(0.5)
    ser.write('0'.encode('utf-8'))
    time.sleep(0.5)
    ser.write('2'.encode('utf-8'))
    time.sleep(0.5)
    ser.write('0'.encode('utf-8'))
    time.sleep(0.5)
    ser.write('2'.encode('utf-8'))
    display("Test","-","Finished Initialized")

def display(mode_name,action,data):
    space = " "
    #out_frame = 60
    print(
        "-----------------------------------------------------------" + "\n" +
        "|" + "Mode: " + mode_name + space * (51-len(mode_name)) + "|" + "\n" +
        "|" + "Sensor: " + action + space + data + space *(47-len(action))  + "|" + "\n" +
        "|" + "Action: " + action + space * (49-len(action)) + "|" + "\n" +
        "-----------------------------------------------------------" + "\n" +
        "\033[5A",end=""
    )

def send_message(message):
    apikey = "DZZO6OWV5Au3DH7u9cdHVtZMfbPh4gHx"
    client = pya3rt.TalkClient(apikey)
    reply_message = client.talk(message)
    return reply_message['results'][0]['reply']

# a_function
def a_bright(data):
    temp = re.sub(r"\D","",data)
    display("Test","brightness",temp)
    if int(temp) > 5:
        jtalk.jtalk("お")
        jtalk.jtalk("明るい")
        car_systems.stop_Stop()
    else:
        jtalk.jtalk("あれ")
        jtalk.jtalk("暗くなっちゃった")
        car_systems.avoid(300)
        

def a_temp(data):
    temp = re.sub(r"\D","",data)
    display("Test","temperature",temp)
    
def a_humi(data):
    humi = re.sub(r"\D","",data)
    display("Test","humidity",temp)

def a_water(count):
    if count == 0:
        display("Test","water_plant","0")
        jtalk.jtalk("喉が乾いたよ")
    else:
        display("Test","water_plant","1")
        jtalk.jtalk("さようなら、人類")
    
def a_human():
    display("Test","detect_human","1")
    jtalk.jtalk("人間がいるよ")
    jtalk.jtalk("人間さん、こんにちは")
    car_systems.go_Right()
    time.sleep(0.5)
    car_systems.go_Left()
    time.sleep(1)
    car_systems.go_Right()
    time.sleep(1)
    car_systems.go_Left()
    time.sleep(1)
    car_systems.go_Right()
    time.sleep(0.5)
    car_systems.stop_Stop()
    
#　random running
schedule.every(1).minutes.do(jtalk.jtalk,t="散歩しようかな")
schedule.every(1).minutes.do(display,mode_name="Test",action="Run",data="Auto avoidance")
schedule.every(1).minutes.do(car_systems.avoid,times=30)

# 定期走行
def run():
     while True:
         schedule.run_pending()
         time.sleep(1)

# 音声入力待機
def listen_talk():
    text,client,streaming_config = gcp_talk.get_talk()
    with text as stream:

        while not stream.closed:
            
            stream.audio_input = []
            
            audio_generator = stream.generator()
            
            requests = (speech.StreamingRecognizeRequest(
                audio_content=content)for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config,
                                                  requests)

            # Now, put the transcription responses to use.
            my_added_text = gcp_talk.listen_print_loop(responses, stream)
            if my_added_text is None :
                pass
            elif "おはよう" in my_added_text:
                ser.write('3'.encode('utf-8'))
                display("Test","Speaking","おはようございます")
                jtalk.jtalk("おはようございます")
            elif ("あなたの名前は" in my_added_text) or ("名前" in my_added_text):
                ser.write('3'.encode('utf-8'))
                display("Test","Speaking","おはようございますよろしくお願いします。")
                jtalk.jtalk("エントと申します。よろしくお願いします。")
            else:
                ser.write('3'.encode('utf-8'))
                reply = send_message(my_added_text)
                display("Test","Speaking",reply)
                jtalk.jtalk(reply)

            if stream.result_end_time > 0:
                stream.final_request_end_time = stream.is_final_end_time
            stream.result_end_time = 0
            stream.last_audio_input = []
            stream.last_audio_input = stream.audio_input
            stream.audio_input = []
            stream.restart_counter = stream.restart_counter + 1
            stream.new_stream = True
            ser.write('2'.encode('utf-8'))
    
#　FBからのセンサーまわり
def sensor():
    water_counter = 0
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1',50007))
            s.listen(1)    
            initialize()
            while True:   
                # FBからのデータ更新待機
                conn,addr = s.accept()
                with conn:                  
                    data = conn.recv(1024)
                    data = str(data)

                    # dataに基づいたアクションを取る
                    if 'bright' in data:
                        ser.write('3'.encode('utf-8'))
                        a_bright(data)

                    elif 'temp' in data:
                        ser.write('3'.encode('utf-8'))
                        a_temp(data)

                    elif 'humi' in data:
                        ser.write('3'.encode('utf-8'))
                        a_humi(data)

                    elif 'human' in data:
                        ser.write('3'.encode('utf-8'))
                        a_human()

                    elif 'water_plant' in data:
                        ser.write('3'.encode('utf-8'))
                        if counter == 0:
                            a_water(0)
                        else:
                            a_water(1)
                        water_counter = 1

                    ser.write('2'.encode('utf-8'))

    except KeyboardInterrupt:
        car_system.stop_Stop()
        ser.write('0'.encode('utf-8'))
        ser.close()

    ser.write('0'.encode('utf-8'))
    ser.close()                   

if __name__ == "__main__":
    thread_run = threading.Thread(target = run)
    thread_main = threading.Thread(target = sensor)
    thread_talk = threading.Thread(target = listen_talk)
    
    thread_run.start()
    thread_main.start()
    thread_talk.start()
