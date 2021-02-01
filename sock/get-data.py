import sys
import socket
import re

data = sys.stdin.readline()
print(type(data))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1',50007))
    if 'bright' in data:
        num = re.sub(r"\D","",data)
        print(type(num))
        s.sendall(b'bright %i' % int(num))
    elif 'bright_h' in data:
        num = re.sub(r"\D","",data)
        print(type(num))
        s.sendall(b'bright_h %i' % int(num))
    elif 'humi' in data:
        num = re.sub(r"\D","",data)
        print(type(num))
        s.sendall(b'humi %i' % int(num))
    elif 'temp' in data:
        num = re.sub(r"\D","",data)
        print(type(num))
        s.sendall(b'temp %i' % int(num))
    elif 'human' in data:
        s.sendall(b'human')
