# -*- coding: utf-8 -*-

import socket
import threading
import time


def tcplink(sock,addr):
    print "Accept new connection from %s:%s..." % addr
    sock.send('Welcome!')
    while True:
        data=sock.recv(1024)
        time.sleep(1)
        if data=='eixt' or not data:
            break
        sock.send('hello,%s!'% data)
    sock.close()
    print 'Connection from %s:%s closed.'%addr

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',9999))
s.listen(5)
print "Waiting for connection.."

while True:
    try:
        sock,addr=s.accept()
        if sock:
            t=threading.Thread(target=tcplink,args=(sock,addr))
            t.start()
    except Exception as e:
        raise e
    

    


        
    
    
