#coding: utf-8:

import os

def jtalk(t):
    cmd = '../higashi/jtalk.sh ' +  '"' +t + '"'
    os.system(cmd)

def test():
    text = 'おはようございます'
    jtalk(text)

if __name__ == '__main__':
    test()
