#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import socket

class Adsl(object):
    def __init__(self):
        
        self.name = '宽带连接'
        self.username = 'hayb@hayb'
        self.password = 'hayb'

    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(5)
    
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)
        time.sleep(5)

    def reconnect(self):
        print('开始重新拨号')
        self.disconnect()
        self.connect()
        print('重新拨号完成')

    def ifconnect(self):
        if os.system('ping -w 2 www.zhihu.com') == 0:
            print('connect')
        else:
            print('not connect')

if __name__ == '__main__':

    adsl = Adsl()
    adsl.reconnect()
    #print('zhihu ip = '+socket.gethostbyname('zhihu.com'))
  