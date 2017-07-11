#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import random
import json
import re
import requests.packages.urllib3 as urllib3
from rk import RClient
from shenhua import Shenhua
from sqlutil import SqlUtil
import traceback
import sys
import base64
from requests_toolbelt.multipart import encoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Register_Avatar(object):
    
    def __init__(self):
        
        self.session = requests.session()
        self.session.verify = False
        self.prefix = '+86'
        self.rk = RClient('x_xiaoge', 'zzx363711', '79525', '58f3ad277c37449e8b6ee9a73048dd30')
        self.authorization = 'oauth '+'8d5227e0aaaa4797a763ac64e0c3b8'
        self.captcha_id = None
        

    def save_token(self, token, phone_no):
        with open('./tokens/'+phone_no,'w')as f:
            json.dump(token,f)


    def load_token(self, phone_no):
        with open('./tokens/'+phone_no)as f:
            return json.load(f)

    def need_captcha(self):
           
        captcha_url = 'https://api.zhihu.com/captcha'
        captcha_headers = {
                'User-Agent':'osee2unifiedRelease/3.50.0 (iPhone; iOS 10.3.1; Scale/2.00)',
                'Authorization':self.authorization,
        }    
        r = self.session.get(captcha_url, headers = captcha_headers, verify = False)
            
        try:
            j = r.json()
            return j['show_captcha']
                
        except:
            print('获取是否需要验证码标志出现错误')
            return None
    
    def get_captcha(self):
        captcha_url = 'https://api.zhihu.com/captcha'
        
        captcha_headers = {
                'User-Agent':'osee2unifiedRelease/3.50.0 (iPhone; iOS 10.3.1; Scale/2.00)',
                'Authorization':self.authorization,
        }   
        
        captcha_data = {
            'height':'60',
            'width':'240'
        }
        r = self.session.put(captcha_url, headers = captcha_headers, data = captcha_data, verify = False)
        #print('status_code = '+str(r.status_code))
        #print('text = '+r.text)
             
        try:
            j = r.json()
            img_base64_str = j['img_base64']
            image_data = base64.b64decode(img_base64_str)
            with open('captcha.jpg', 'wb') as f:
                f.write(image_data)
                f.close()
        except:
            print('获取验证码失败')
            return None
            
            
        im = open('captcha.jpg', 'rb').read()
        rk_result = self.rk.rk_create(im, 3040)
        self.captcha_id = rk_result['Id']
        captcha = rk_result['Result']
        print('打码平台识别出的验证码为：'+captcha)
        return self.captcha_id, captcha
    
    def validate_captcha(self, captcha):
        captcha_url = 'https://api.zhihu.com/captcha'
        
        captcha_headers = {
                'User-Agent':'osee2unifiedRelease/3.50.0 (iPhone; iOS 10.3.1; Scale/2.00)',
                'Authorization':self.authorization,
        }  
    
        captcha_data = {'input_text':captcha}
        r = self.session.post(captcha_url, headers = captcha_headers, data = captcha_data, verify = False)
            
        if r.status_code == 201:
            return True
        else:
            print('验证码校验失败')
            return False
    
    def validate(self, phone_no):
        #print('phone_no = '+phone_no)
        validate_api_url = 'https://api.zhihu.com/validate/register_form'
        validate_headers = {
            'User-Agent':'osee2unifiedRelease/3.50.0 (iPhone; iOS 10.3.1; Scale/2.00)',
            'Authorization':self.authorization,
            }
        validate_data = {'fullname':phone_no,
                         'password':phone_no,
                         'phone_no':self.prefix + phone_no
                        }
    
        r = self.session.post(validate_api_url, headers = validate_headers, data = validate_data, verify = False)
        #cookies_str = json.dumps(session.cookies.get_dict())
        #print('cookies_str = '+str(cookies_str))
        #print('validate_status = '+str(r.status_code))
        #print('validate_text = '+r.text)
        
        if(r.status_code == 200):
            try:
                success = r.text.index('success')
            except:
                success = -1
            #print('success = '+str(success))
            
            if success > 0:
                print('手机号:'+phone_no+'在知乎验证通过，可以注册')
                return True
            else:
                print('手机号:'+phone_no+'在知乎已被注册')
                return False
           
    
    def send_message(self, phone_no):
       
        message_api_url = 'https://api.zhihu.com/sms/digits'
        message_headers = {
            
            'Authorization':self.authorization,
            
            
            'User-Agent':'osee2unifiedRelease/3.34.0 (iPhone; iOS 10.2; Scale/2.00)',
            
            #'Cookie':'capsion_ticket="2|1:0|10:1493013544|14:capsion_ticket|44:MzI3YzlkNDQyMWYxNDJmOThhY2U0MGJkMzBkOWY1OGM=|9505a6f728c79702698d566e63b84055b1ebdbcb80ac75d380cb391cc8837ac9"'
            
            }
        message_data = {'phone_no': self.prefix + phone_no}
    
        r = self.session.post(message_api_url, headers = message_headers, data = message_data, verify = False)
     
       
        if(r.status_code == 201):
            try:
                success = r.text.index('success')
            except:
                success = -1
            #print('success = '+str(success))
            if success > 0:
                print('知乎已经发送手机验证码')
                return True
            else:
                print('知乎发送手机验证码失败')
                print('message_status = '+str(r.status_code))
                print('message_text = '+r.text)
                return False
        else:
            print('知乎发送手机验证码失败，错误信息如下：')
            print('message_status = '+str(r.status_code))
            print('message_text = '+r.text)
            self.rk.rk_report_error(self.captcha_id)
            return False
    
    def register(self, phone_no, password, fullname, avatarUrl, digits):
        
    
        register_api_url = 'https://api.zhihu.com/register'
        register_headers = {
            'Authorization':self.authorization,
            'User-Agent':'osee2unifiedRelease/3.34.0 (iPhone; iOS 10.2; Scale/2.00)',
            }
        #session.cookies.clear()
        #cookies_str = json.dumps(session.cookies.get_dict())
        #print('cookies_str = '+str(cookies_str))
        #print('digits = '+digits)
        
        register_data = {'digits':digits,
                         'fullname':fullname,
                         'password':password,
                         'phone_no':self.prefix + phone_no,
                         'register_type':'phone_digits'
                        }
        
        
        r = self.session.post(register_api_url, headers = register_headers, data = register_data, verify = False)
        
        if(r.status_code == 201):
            token = r.json()
            
    
            print('手机号:'+phone_no+' 注册成功')
            
            #self.save_token(token, phone_no)
            self.upload_avatar(token, avatarUrl)
            return True
        else:
            print('手机号:'+phone_no+'注册失败')
            print('注册出现异常:')
            print('register_status = '+str(r.status_code))
            print('register_text = '+r.text)
            
            return False
        
    def download_avatar(self, avatarUrl):
       
        print('avatarUrl = '+avatarUrl) 
        
        index = avatarUrl.rindex('/')
        avatarName = avatarUrl[index+1:]
        headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }
        r = self.session.get(avatarUrl, headers=headers, verify = False)
        with open('./avatars/'+avatarName, 'wb') as f:
            f.write(r.content)
            f.close()
            
        return avatarName
       
    def upload_avatar(self, token, avatarUrl):
        print('开始下载头像')
        avatarName = self.download_avatar(avatarUrl)
        print('开始上传头像')
        avatar_api_url = 'https://api.zhihu.com/people/self/avatar'
     
        token_type=str(token['token_type'].capitalize())
        access_token=str(token['access_token'])
    
        avatar_headers = {
            'Authorization': '{type} {token}'.format(type=token_type,token=access_token),
            'User-Agent': 'osee2unifiedRelease/3.50.0 (iPhone; iOS 10.3.1; Scale/2.00)',
        }
        
       
        
        files = {
            'picture': ("image.jpeg", open('./avatars/'+avatarName, 'rb'), 'image/jpeg')
        }
        avatar_data = encoder.MultipartEncoder(files)
        avatar_headers["Content-Type"] = avatar_data.content_type
        #session.cookies.clear()
        #cookies_str = json.dumps(session.cookies.get_dict())
        #print('cookies_str = '+str(cookies_str))
       
        
        r = self.session.post(avatar_api_url, headers = avatar_headers, data = avatar_data, verify = False)
        
       
        if r.status_code == 201:
            print('上传成功')
        else:
            print('上传失败')
            print('avatar_status = '+str(r.status_code))
            print('avatar_text = '+r.text)
        
        
    def register_task(self, task_count):
        
        sqlUtil = SqlUtil()
        shenhua = Shenhua()
        success_count = 0
      
        for i in range(task_count * 2):
            print(' ')
            print('开始注册第 '+str(i + 1)+' 个账号')
            
            phone_no = shenhua.get_phone()
            password = chr(random.randint(97, 122)) + chr(random.randint(97, 122)) + chr(random.randint(97, 122)) + chr(random.randint(97, 122))  + str(random.randint(0, 9))+ str(random.randint(0, 9))+ str(random.randint(0, 9))+ str(random.randint(0, 9))
            
            fullname, avatar = sqlUtil.get_fullname_avatar()
            #dbutil.insert_register(phone_no, password, phone_no, 'N', task_id)
            need_captcha_flag = self.need_captcha()
     
            if self.validate(phone_no):
                #dbutil.update_status(phone_no, 'V', 'Validate')
                if need_captcha_flag:
                   captcha_id, captcha = self.get_captcha()
                   self.validate_captcha(captcha)

                if self.send_message(phone_no):
                    time.sleep(15)
                    digits = shenhua.get_message(phone_no)
                    if digits != None:
                        #dbutil.update_verification_code(phone_no, digits)
                        if self.register(phone_no, password, fullname, avatar, digits):
                            #dbutil.update_status(phone_no, 'S', 'Success')
                            sqlUtil.insert_account(phone_no, password, 'phone', '注册的账号')
                            success_count += 1
                            #current_count += 1
                            #dbutil.update_tasks(task_id, current_count,  'P')
                        #else:
                        #    dbutil.update_status(phone_no, 'E', 'Error')
                    #if current_count >= end_count:
                    #    dbutil.update_tasks(task_id, current_count,  'S')
                       
                    #    break
            #time.sleep(5)
        print(' ')
        print('本次注册成功的个数：'+str(success_count))
        #dbutil.close()
    

if __name__ == '__main__':
    
    register = Register()
    
    register.register_task(10)