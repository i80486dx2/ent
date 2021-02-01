from schedule import *
import schedule
import time

num = 0

def hello():
    global num
    num += 1
    print("hello {}".format(num))

def test(t,n):
    print(t)
    print(n)
    
schedule.every(1).second.do(hello)
schedule.every(1).second.do(test,"yes","no")
while True:
    schedule.run_pending()
    time.sleep(1)
