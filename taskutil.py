# -*- coding: utf-8 -*-

import requests
import random
import re
import os
import json
import time
from rk import RClient

user_agent_list = [
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
]



class TaskUtil(object):
    
    def __init__(self, answerURL, username, password):
        self.rk = RClient('x_xiaoge', 'zzx363711', '79525', '58f3ad277c37449e8b6ee9a73048dd30')
        self.session = requests.session()
        self.base_url = "https://www.zhihu.com/"
        self.session.headers["User-Agent"] = random.choice(user_agent_list)
        self.session.headers["Referer"] = self.base_url
        self.session.headers["Host"] = "www.zhihu.com"
        self.session.get(self.base_url)
        self.answerURL = answerURL
        self.username = username
        self.password = password
        self.session.cookies.clear()
        self.session.cookies.update(self.get_cookie())
        
        
    def isLogin(self):
        # 通过查看用户个人信息来判断是否已经登录成功
        profile_url = "https://www.zhihu.com/settings/profile"
        test_login = self.session.get(profile_url, allow_redirects=False)
        if test_login.status_code == 200:
            return True
        else:
            return False
    
    def get_xsrf(self):
        url = 'https://www.zhihu.com'
        # 获取登录时需要用到的_xsrf
        index_page = self.session.get(url)
        html = index_page.text
        pattern = r'name="_xsrf" value="(.*?)"'
        # 这里的_xsrf 返回的是一个list
        results = re.findall(pattern, html)
        if len(results) < 1:
            print('提取XSRF 代码失败')
            return None
        return results[0]
    
    # 获取验证码
    def get_captcha(self):
        t = str(int(time.time()*1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self.session.get(captcha_url)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
    
        im = open('captcha.jpg', 'rb').read()
        
        rk_result = self.rk.rk_create(im, 3040)
        captcha_id = rk_result['Id']
        captcha = rk_result['Result']
        
        print('打码平台识别出的验证码为：'+captcha)
        return captcha_id, captcha
    
    def save_cookie(self):
        with open('./cookies/'+self.username,'w')as f:
            json.dump(self.session.cookies.get_dict(),f)

    def read_cookie(self):
        with open('./cookies/'+self.username)as f:
            cookie=json.load(f)
        return cookie
    
    
    def login(self):
        #print('in login')
        if re.match(r"^1\d{10}$", self.username): 
            #print("手机号登录 \n")
            login_url = 'https://www.zhihu.com/login/phone_num'
            account_type = "phone_num"
        
        elif re.match(r"^\S+\@\S+\.\S+$", self.username): 
            #print("邮箱登录 \n")
            login_url = 'https://www.zhihu.com/login/email'
            account_type = "email"
        else:
            pass
            print("错误的账号类型，跳过本账号，开始执行下一条记录 \n")
            #to do 更新账号状态
            return None
        captcha_id, captcha = self.get_captcha()
        login_data = {
            '_xsrf':self.get_xsrf(),
            account_type: self.username,
            'password': self.password,
            'remember_me': 'true',
            'captcha':captcha
        }
    

        r = self.session.post(login_url, data = login_data, verify = False)
        status_code = r.status_code
        if int(status_code) == 200:
            #print('taskutil login r_text = '+r.text)
            try:
                j=r.json()
                code = int(j['r'])
                if code == 0:
                    print('账户:' + self.username +'登录成功')
                    self.save_cookie()
            except:
                print('账户:' + self.username +'状态异常，无法创建cookie')
                #to do 更新账户状态
        else:
            print('账户:' + self.username +'登录失败')
        
        return self.session.cookies.get_dict()
            
    def get_cookie(self):
        
        if os.path.exists('./cookies/'+self.username):
            cookie = self.read_cookie()
            #print('cookie = '+str(cookie))
            self.session.cookies.update(cookie)
            if self.isLogin():
                print('账户:' + self.username +'的cookie在有效期内，无需重新登录')
                cookie =  cookie
            else:
                print('账户:' + self.username +'的cookie已失效，重新登录')
                cookie =  self.login()
        else:
            print('账户:' + self.username +'的cookie不存在，需要登录')
            cookie =  self.login()
        return cookie
    
    
    #def get_cookie(self):
    #    with open(self.cookie_file) as fr:
    #        return json.loads(fr.read())
        
        
    def get_id(self):
        """ 获取要点赞回答的 ID, 回答所在的问题的 ID, 以及随机一个回答所在话题的 ID
        Arguments:
            answerURL -- str
            answerURL=https://www.zhihu.com/question/55761843/answer/181595645
        return:
        answerid --- str
        questionid --- str
        topicid --- str
        """
        try:
            self.session.headers["X-Requested-With"] = None
            self.session.headers["X-Xsrftoken"] = None

            response = self.session.get(self.answerURL, timeout=4)
            response.encoding = response.apparent_encoding

            pa = r'href="/topic/(\d+)"'
            res = re.findall(pa, response.text)
            if res:
                topicID = random.choice(res)
            else:
                topicID = None
            questionID = re.findall(r'data-id="(\d+)">关注问题', response.text)
            if questionID:
                questionID = questionID[0]
            else:
                questionID = None
            answerID = re.findall(r'answer-id" content="(\d+)"', response.text)
            if answerID:
                answerID = answerID[0]
            else:
                answerID = None
        except Exception as e:
            print(e)
            answerID = None
            topicID = None
            questionID = None

        return answerID, questionID, topicID
    
    def follow_topic(self, topicID):
        # try:
            if topicID:
                return "已经关注过该话题"
                topicURL = "https://www.zhihu.com/topic/%s/hot" % topicID
                self.session.headers["X-Requested-With"] = None
                self.session.headers["X-Xsrftoken"] = None
                self.session.headers["Referer"] = self.answerURL
            r = self.session.get(topicURL, timeout=4)
            r.encoding = r.apparent_encoding
            topicFollowURL = "https://www.zhihu.com/node/TopicFollowBaseV2"
            pa = r'id="tf-tf-(\d+)"'
            topic_follow_id = re.findall(pa, r.text)[0]

            params = {
                "method": "follow_topic",
                "params": '{"topic_id":"%s"}' % topic_follow_id
            }
            self.session.headers["X-Requested-With"] = "XMLHttpRequest"
            self.session.headers["X-Xsrftoken"] = self.session.cookies.get_dict()['_xsrf']
            self.session.headers["Referer"] = topicURL
            response = self.session.post(topicFollowURL, data=params, timeout=4)
            if response.json()['r'] == 0:
                return "成功关注话题"
        # except Exception as e:
        #     return "关注话题失败"

    def follow_question(self, questionID):
        try:
            if not questionID:
                return "已经关注该问题"
            follow_questionURL = 'https://www.zhihu.com/node/QuestionFollowBaseV2'
            params = {
                "method": "follow_question",
                "params": '{"question_id":"%s"}' % questionID
            }
            self.session.headers["X-Requested-With"] = "XMLHttpRequest"
            self.session.headers["X-Xsrftoken"] = self.session.cookies.get_dict()['_xsrf']
            self.session.headers["Referer"] = self.answerURL
            response = self.session.post(follow_questionURL, data=params, timeout=4)
            if response.json()['r'] == 0:
                return "成功问题成功"
        except Exception as e:
            return "关注问题失败"

    def vote_answer(self):
        answerID, questionID, topicID = self.get_id()
        try:
            if not answerID:
                return 'E', '获取answerID出错', -1
            answerVoteURL = "https://www.zhihu.com/node/AnswerVoteBarV2"
            postdata = {
                "method": "vote_up",
                "params": '{"answer_id":"%s"}' % answerID
            }
            self.session.headers["X-Requested-With"] = "XMLHttpRequest"
            self.session.headers["X-Xsrftoken"] = self.session.cookies.get_dict()['_xsrf']
            self.session.headers["Referer"] = self.answerURL
            r = self.session.post(answerVoteURL, data=postdata, timeout=4)
            r.encoding = r.apparent_encoding
            #print('taskutil vote_answer r_text '+r.text)
            if r.json()['r'] == 0:
                current_count = 0
                params = {
                    "params": '{"answer_id":"%s"}' % answerID
                }
               
                self.session.headers["X-Xsrftoken"] = None
             
                answerVoteInfoURL = "https://www.zhihu.com/node/AnswerVoteInfoV2"
                rnum = self.session.get(answerVoteInfoURL, params=params, timeout=10)
               
                rnum.encoding = rnum.apparent_encoding
                pa = r'data-votecount="(\d+)"'
                vote_num = re.findall(pa, rnum.text)
                if vote_num:
                    current_count =  vote_num[0]
                else:
                    current_count = -1
                print('点赞成功，当前赞数：'+str(current_count))
                return 'S', '点赞成功', current_count
            elif r.json()['r'] == 1:
                if r.json()['errcode'] == 1002:
                    print('账户:'+self.username+'状态异常，异常信息：您的帐号由于存在异常行为暂时被知乎反作弊系统限制使用')
                    return 'E', '您的帐号由于存在异常行为暂时被知乎反作弊系统限制使用', -1
        except Exception as e:
            return 'E', '未知异常', -1
        
    def get_current_count(self):
        answerID, questionID, topicID = self.get_id()
        current_count = 0
        params = {
            "params": '{"answer_id":"%s"}' % answerID
        }
       
        self.session.headers["X-Xsrftoken"] = None
     
        answerVoteInfoURL = "https://www.zhihu.com/node/AnswerVoteInfoV2"
        r = self.session.get(answerVoteInfoURL, params=params, timeout=10)
       
        r.encoding = r.apparent_encoding
        pa = r'data-votecount="(\d+)"'
        vote_count = re.findall(pa, r.text)
        if vote_count:
            current_count =  vote_count[0]
        else:
            current_count = -1
        
        return current_count
    
    def set_guide_headline(self, headline):
        url = "https://www.zhihu.com/node/Guide2"
        self.session.headers["X-Requested-With"] = "XMLHttpRequest"
        self.session.headers["X-Xsrftoken"] = self.session.cookies.get_dict()['_xsrf']

        params = {
            "method": "add_headline",
            "params": '{"headline":"%s"}' % headline
        }
        self.session.post(url, data=params)
        params = {
            "method": "dismiss_editor",
            "params": '{"key":"bio"}'
        }
        self.session.post(url, data=params)
        
if __name__ == '__main__':
    
    answerURL = 'https://www.zhihu.com/question/19677738/answer/186073084'
    username = '13631753183'
    password = 'yyut8603'
    
    taskUtil = TaskUtil(answerURL, username, password)
  
    #vote_status, vote_msg = taskUtil.vote_answer()
    #print('vote_status = '+vote_status)
    current_count = taskUtil.get_current_count()
    print('current_count = '+str(current_count))
    
    
   
    
   
    