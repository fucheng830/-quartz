# coding: utf-8  

import os  
try:  
    import fcntl  
    LOCK_EX = fcntl.LOCK_EX  
except ImportError:  
    # 
    fcntl = None  
    import win32con  
    import win32file  
    import pywintypes  
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK  
    overlapped = pywintypes.OVERLAPPED()
  
class Lock:  
    """
    """  
      
    def __init__(self, filename='processlock.txt'):  
        self.filename = filename  
        # 
        self.handle = open(filename, 'w')  
  
    def acquire(self):  
        # 
        if fcntl:  
            fcntl.flock(self.handle, LOCK_EX)  
        else:  
            hfile = win32file._get_osfhandle(self.handle.fileno())  
            win32file.LockFileEx(hfile, LOCK_EX, 0, -0x10000, overlapped)  
  
    def release(self):  
        # 
        if fcntl:  
            fcntl.flock(self.handle, fcntl.LOCK_UN)  
        else:  
            hfile = win32file._get_osfhandle(self.handle.fileno())  
            win32file.UnlockFileEx(hfile, 0, -0x10000, overlapped)  
  
    def __del__(self):  
        try:  
            self.handle.close()  
            os.remove(self.filename)  
        except:  
            pass  
  
if __name__ == '__main__':  
    # 
    import time  
    print 'Time: %s' % time.time()  
  
    lock = Lock()  
    try:  
        lock.acquire()  
        time.sleep(20)  
    finally:   
        lock.release()  
  
    print 'Time: %s' % time.time()  