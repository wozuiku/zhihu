#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import time
import json
import os.path
import configparser



class Shenhua(object):

    def __init__(self):
        
        self.api_url = 'http://api.shjmpt.com:9002/pubApi'
        self.developer_key = 'zzx363711'
        self.username = 'x_xiaoge'
        self.password = 'zzx363711'
        r = requests.get(self.api_url+'/uLogin', params={'uName':self.username, 'pWord':self.password})
        try:
            self.token = r.text[0:r.text.index('&')]
        except:
            print ("从神话平台获取token失败，返回信息为："+r.text)
                
        
       

    def get_phone(self):
        r = requests.get(self.api_url+'/GetPhone', params={'ItemId':9389, 'token': self.token})
        #print('r.status_code = '+str(r.status_code))
        #print('text = ' + r.text)
        #mobile = r.text[r.text.index('mobile') + 9:r.text.index('gold') - 3]
        #print('mobile = '+mobile)
        phone = r.text[0:len(r.text) - 1]
        print('从神话平台取到的手机号为: ' + phone)
        return phone
        
    def get_message(self, phone):
        r = requests.get(self.api_url+'/GMessage', params={'token': self.token,'ItemId':9389, 'Phone':phone})
        #print('r.status_code = '+str(r.status_code))
        #print('text = ' + r.text)
        print('神话平台收到知乎的信息为: ' + r.text)
        try:
            verification_code = r.text[r.text.index('是')+2:r.text.index('分钟')-4]
            print('从神话平台取到的验证码为: ' + verification_code)
        except:
            verification_code = None
            print('从神话平台取到的验证码异常')
        
        return verification_code
    
if __name__ == '__main__':
    msg = '神话平台收到知乎的信息为: MSG&9389&13902775417&【知乎】创建帐号的验证码是 401846，10 分钟内有效。'
    verification_code = msg[msg.index('是')+2:msg.index('是')+8]
    print('从神话平台取到的验证码为: ' + verification_code)
    
    

