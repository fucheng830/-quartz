# -*- coding: utf-8 -*-

import glob 
import os
import time,threading


'''
def path():
    abs_path=os.path.abspath('..')
    for i in glob.glob("%s\data\*.pkl"%abs_path):
        print i
    

# 新线程执行的代码:
def loop():
    print 'thread %s is running...' % threading.current_thread().name
    n = 0
    while n < 5:
        n = n + 1
        print 'thread %s >>> %s' % (threading.current_thread().name, n)
        time.sleep(1)
    print 'thread %s ended.' % threading.current_thread().name

print 'thread %s is running...' % threading.current_thread().name
t1 = threading.Thread(target=loop, name='LoopThread')
t2 = threading.Thread(target=path, name='pathThread')
t1.start()
t1.join()
t2.start()
t2.join()

print 'thread %s ended.' % threading.current_thread().name
'''

from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())

if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    p = Process(target=run_proc, args=('test',))
    print 'Process will start.'
    p.start()
    p.join()
    print 'Process end.'
    