# -*- coding: utf-8 -*-
import sqlite3
import csv
import random


class SqlUtil(object):
    
    def __init__(self):
        
        self.conn = None
        
    
    def connect(self):
        
        self.conn = sqlite3.connect('zhihu.db')
        
    def create_account_table(self):
        self.connect()
        try:
            self.conn.execute('''CREATE TABLE account
               (id         INTEGER PRIMARY KEY    AUTOINCREMENT ,
                type       CHAR(20),
                username   CHAR(50),
                password   CHAR(50),
                fullname   CHAR(100),
                avatarUrl  CHAR(100),
                link        CHAR(100),
                headline   CHAR(100),
                location  CHAR(100),
                business   CHAR(100),
                employment CHAR(100),
                education CHAR(100),
                description CHAR(200),
                sinaWeiboUrl CHAR(100),
                gender     CHAR(10),
                avatar     CHAR(10),
                status     CHAR(10),
                remark     CHAR(100),
                create_time     TIMESTAMP default (datetime('now', 'localtime'))   );''')
            
        except:
            pass
        
        self.conn.close()
        
    def create_task_table(self):
        self.connect()
        try:
            self.conn.execute('''CREATE TABLE task
               (id         INTEGER PRIMARY KEY    AUTOINCREMENT ,
                type       CHAR(20)  ,
                task_url   CHAR(200)  ,
                task_count     CHAR(20)  ,
                begin_count    CHAR(20)  ,
                current_count  CHAR(20)  ,
                status     CHAR(10) ,
                task_order     CHAR(20) ,
                task_interval     CHAR(20) ,
                customer   CHAR(100) ,
                deliver     CHAR(10) ,
                remark     CHAR(200) ,
                create_time     TIMESTAMP default (datetime('now', 'localtime'))
                 );''')
        except:
            pass
        
        
        self.conn.close()
        
    
    def create_history_table(self):
        self.connect()
        try:
            self.conn.execute('''CREATE TABLE history
               (id         INTEGER PRIMARY KEY    AUTOINCREMENT ,
                task_url   CHAR(200)  ,
                user_name     CHAR(60)  ,
                status     CHAR(10) ,
                create_time     TIMESTAMP default (datetime('now', 'localtime'))
                 );''')
        except:
            pass
        self.conn.close()
    
    def create_setting_table(self):
        self.connect()
        try:
            self.conn.execute('''CREATE TABLE setting
               (id         INTEGER PRIMARY KEY    AUTOINCREMENT ,
                type       CHAR(20)   ,
                value1       CHAR(60)   ,
                value2       CHAR(60)   ,
                value3      CHAR(60)  );''')
            
        except:
            pass
        
        self.conn.close()
        
    def create_zhihu_user_info_table(self):
        self.connect()
        try:
            self.conn.execute('''CREATE TABLE zhihu_user_info
               (id         INTEGER PRIMARY KEY    AUTOINCREMENT ,
                name       CHAR(100)  ,
                avatarUrl   CHAR(200)  ,
                link        CHAR(200)  ,
                headline     CHAR(200) ,
                location     CHAR(100) ,
                business     CHAR(100) ,
                employment CHAR(100),
                education     CHAR(100) ,
                description     CHAR(600) ,
                sinaWeiboUrl CHAR(200),
                gender     CHAR(20),
                create_time     TIMESTAMP default (datetime('now', 'localtime'))
                 );''')
        except:
            pass
        
        
        self.conn.close()
                
    def drop_task_table(self):
        self.connect()
        self.conn.execute('''DROP TABLE task''')
        self.conn.close()
            
        
    def drop_account_table(self):
        self.connect()
        self.conn.execute('''DROP TABLE account''')
        self.conn.close()
    
    def drop_history_table(self):
        self.connect()
        self.conn.execute('''DROP TABLE history''')
        self.conn.close()

    def drop_setting_table(self):
        self.connect()
        self.conn.execute('''DROP TABLE setting''')
        self.conn.close()
        
    def drop_zhihu_user_info_table(self):
        self.connect()
        self.conn.execute('''DROP TABLE zhihu_user_info''')
        self.conn.close()
        
    def check_account(self, username):
        self.connect()
        select_sql = "SELECT id, username, password, type, status, remark FROM account WHERE username = '%s'" % (username)
        cursor = self.conn.execute(select_sql)
        if len(cursor) > 0:
            print('exists')
            return True
        
        self.conn.close()
        
    def insert_task(self, type, task_url, task_count, begin_count, current_count,  status,  task_order, task_interval, customer, deliver, remark):
        
        self.connect()
        
        insert_sql = "INSERT INTO task(type, task_url, task_count, begin_count, current_count, status, task_order, task_interval, customer, deliver, remark)  VALUES ( \'"+type+"',\'" +task_url+ "\',\'" +task_count+ "\',\'" +begin_count+ "\' ,\'" +current_count+ "\',\'" +status+ "\',\'" +task_order+ "\',\'" +task_interval+ "\',\'" +customer+ "\',\'" +deliver+ "\',\'" +remark+ "\')" 
        #print('insert_sql = '+insert_sql)
        self.conn.execute(insert_sql)
        self.conn.commit()
        self.conn.close()
        
    def select_task(self):
        self.connect()
        select_sql = 'SELECT id, type, task_url, task_count, begin_count, current_count, status,  task_order, task_interval, customer, deliver, remark, create_time FROM task'
        cursor = self.conn.execute(select_sql)
        
        tasks = []
        
        for row in cursor:
            
            tasks.append(row)
            
        self.conn.close()
        
        return tasks
    
    def delete_task(self, taskUrl):
        self.connect()
        delete_sql = "DELETE FROM  task  WHERE task_url = '%s'" % (taskUrl)
        cursor = self.conn.execute(delete_sql)
        self.conn.commit()        
        self.conn.close()
        
    def query_tasks(self, type, task_url, task_count, begin_count, current_count,  status, task_order, task_interval, customer, deliver, remark):
        self.connect()
        select_sql = "SELECT id, type, task_url, task_count, begin_count,current_count, status,  task_order, task_interval, customer, deliver, remark, create_time FROM task WHERE type LIKE '%"+type+"%' AND task_url LIKE '%"+task_url+"%' AND task_count LIKE '%"+task_count+"%' AND begin_count LIKE '%"+begin_count+"%' AND current_count LIKE '%"+current_count+"%' AND status LIKE '%"+status+"%' AND task_order LIKE '%"+task_order+"%' AND task_interval LIKE '%"+task_interval+"%' AND customer LIKE '%"+customer+"%' AND deliver LIKE '%"+deliver+"%' AND remark LIKE '%"+remark+"%' "
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        tasks = []
        for row in cursor:
            tasks.append(row)
            
        self.conn.close()
        
        return tasks
    
    def get_pending_task(self):
        self.connect()
        select_sql = "SELECT id, type, task_url, task_count, begin_count, current_count,  task_interval FROM task WHERE  status = '待执行'"
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        
        tasks = []
        
        for row in cursor:
            tasks.append(row)
            
        self.conn.close()
        
        if len(tasks) > 0:
            return tasks[0]
        else:
            return None
    
    def get_task_begin_count(self, task_url):
        self.connect()
        select_sql = "SELECT begin_count FROM task WHERE  task_url = '"+task_url+"'"
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        begin_count = '0'
        for row in cursor:
            begin_count = row[0]
        self.conn.close()
        return begin_count
    
    def get_task_current_count(self, task_url):
        self.connect()
        select_sql = "SELECT current_count FROM task WHERE  task_url = '"+task_url+"'"
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        current_count = '0'
        for row in cursor:
            current_count = row[0]
        self.conn.close()
        return current_count
    
    def get_pending_accounts(self, task_url):
        
        #print('get_pending_accounts')
        
        self.connect()
        select_sql = "SELECT id, username, password, avatar, avatarUrl, headline FROM account WHERE status = '正常' AND NOT EXISTS(SELECT 'x' FROM history WHERE task_url = '"+task_url+"' AND user_name = username)"
        #select_sql = "SELECT id, username, password FROM account WHERE status = '正常' "
        
        cursor = self.conn.execute(select_sql)
        
        accounts = []
        
        for row in cursor:
            
            accounts.append(row)
            
        self.conn.close()
        
        return accounts
        
    def get_random_account(self):
        
        self.connect()
        select_sql = "SELECT id, username, password FROM account WHERE status = '正常' "
        cursor = self.conn.execute(select_sql)
        accounts = []
        
        
        
        for row in cursor:
            
            accounts.append(row)
            
        self.conn.close()
        
        i = random.randint(0, len(accounts) - 1)
        
        return accounts[i]    
    
    def query_task(self, id):
        self.connect()
        select_sql = "SELECT id, type, task_url, task_count, begin_count, current_count, status,  task_order, task_interval, customer, deliver, remark, create_time FROM task WHERE id = "+id
        print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        task = []
        for row in cursor:
            task.append(row)
        
        self.conn.close()
        
        return task
    
    def update_task(self, type, task_url, task_count, begin_count, current_count, status, task_order, task_interval, customer, deliver, remark, id):
        self.connect()
        update_sql = "UPDATE task SET type = '"+type+"', task_url = '"+task_url+"',task_count = '"+task_count+"',begin_count = '"+begin_count+"',current_count = '"+current_count+"',status = '"+status+"',task_order = '"+task_order+"',task_interval = '"+task_interval+"',customer = '"+customer+"',deliver = '"+deliver+"',remark = '"+remark+"'   WHERE id = " + id
        cursor = self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()
    
    def update_task_batch(self, status, task_order, task_interval, deliver, id):
        self.connect()
        update_sql = "UPDATE task SET status = '"+status+"',task_order = '"+task_order+"',task_interval = '"+task_interval+"' ,deliver = '"+deliver+"'  WHERE id = " + id
        cursor = self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()  
        
    def update_task_status(self, status, id):
        self.connect()
        update_sql = "UPDATE task SET status = '"+status+"'  WHERE id = " + id
        self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()  
        
    def update_task_begin_count(self, begin_count, id):
        self.connect()
        update_sql = "UPDATE task SET begin_count = '"+begin_count+"'  WHERE id = " + id
        self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()    
        
    def update_task_current_count(self, current_count, id):
        self.connect()
        update_sql = "UPDATE task SET current_count = '"+current_count+"'  WHERE id = " + id
        self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()   
        
                    
    def insert_account(self, username, password, fullname, avatarUrl, type, avatar, status, remark):
        
        
        self.connect()
        
        insert_sql = "INSERT INTO account(username, password, fullname, avatarUrl,type, avatar, status, remark)  VALUES ( \'"+username+"',\'" +password+ "\',\'"+fullname+"',\'" +avatarUrl+ "\',\'" +type+ "\',\'" +avatar+ "\',\'" +status+ "\',\'" +remark+ "\')" 
        
        self.conn.execute(insert_sql)
        self.conn.commit()
        self.conn.close()
        
    def select_account(self):
        self.connect()
        select_sql = 'SELECT id, username, password, type,avatar, status, remark FROM account'
        cursor = self.conn.execute(select_sql)
        
        accounts = []
        
        for row in cursor:
            
            accounts.append(row)
            
        self.conn.close()
        
        return accounts
    
    def query_accounts(self, type, username, password, avatar, status, remark):
        self.connect()
        select_sql = "SELECT id, username, password, type,avatar, status, remark FROM account WHERE type LIKE '%"+type+"%' AND username LIKE '%"+username+"%' AND password LIKE '%"+password+"%' AND avatar LIKE '%"+avatar+"%' AND status LIKE '%"+status+"%' AND remark LIKE '%"+remark+"%' "
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        
        accounts = []
        
        for row in cursor:
            
            accounts.append(row)
            
        self.conn.close()
        
        return accounts
        
    def update_account(self, username, status, errMsg):
        self.connect()
        update_sql = "UPDATE account SET status = '"+status+"' , remark = '"+errMsg+"'  WHERE username = '"+username+"'" 
        cursor = self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()
        
    def delete_account(self, username):
        self.connect()
        delete_sql = "DELETE FROM  account  WHERE username = '%s'" % (username)
        cursor = self.conn.execute(delete_sql)
        self.conn.commit()        
        self.conn.close()

    def insert_history(self, task_url, user_name, status):
        
        self.connect()
        
        insert_sql = "INSERT INTO history(task_url, user_name, status)  VALUES ( \'"+task_url+"',\'" +user_name+ "\',\'" +status+ "\')" 
        
        self.conn.execute(insert_sql)
        self.conn.commit()
        self.conn.close()

    def select_history(self):
        self.connect()
        select_sql = 'SELECT task_url, user_name, status FROM history'
        cursor = self.conn.execute(select_sql)
        historys = []
        for row in cursor:
            historys.append(row)
        self.conn.close()
        
        return historys
        
    def insert_setting(self, type, value1, value2, value3):
        
        self.connect()
        
        insert_sql = "INSERT INTO setting(type, value1, value2, value3)  VALUES ( \'"+type+"',\'" +value1+ "\',\'" +value2+ "\',\'" +value3+ "\')" 
        
        self.conn.execute(insert_sql)
        self.conn.commit()
        self.conn.close()
        
    def update_setting(self, type, value1, value2, value3):
        self.connect()
        update_sql = "UPDATE setting SET value1 = '"+value1+"', value2 = '"+value2+"',value3 = '"+value3+"'   WHERE type = '" + type +"'"
        #print('update_sql = '+update_sql)
        cursor = self.conn.execute(update_sql)
        self.conn.commit()        
        self.conn.close()
    
    def select_setting(self):
        self.connect()
        select_sql = 'SELECT type, value1, value2, value3 FROM setting'
        cursor = self.conn.execute(select_sql)
        
        settings = []
        for row in cursor:
            settings.append(row)
        self.conn.close()
        
        return settings
    
    def sava_setting(self, type, value1, value2, value3):
        
        settings = self.query_settings(type)
        
        if len(settings) == 0:
            self.insert_setting(type, value1, value2, value3)
            
        elif len(settings) > 0:
            self.update_setting(type, value1, value2, value3)
        
    
    def query_settings(self, type):
        self.connect()
        select_sql = "SELECT  value1, value2, value3 FROM setting WHERE type LIKE '%"+type+"%' "
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        settings = []
        for row in cursor:
            settings.append(row)
        self.conn.close()
        
        return settings   
    
    def read_csv(self, fn='data1.csv'):
    
        with open(fn, encoding="utf-8") as fr:
            csvfr = csv.reader(fr)
            rows = [row for row in csvfr]
        return rows
    
    def insert_zhihu_user_info(self):
        
        self.connect()
        rows = self.read_csv('./data/zhihu_user_info.csv')
        del rows[0]
        for row in rows:
            #print('row[0] = '+row[0]) 
            try: 
                insert_sql = "INSERT INTO zhihu_user_info(name, avatarUrl, link, headline, location, business, employment, education, description, sinaWeiboUrl)  VALUES ( \'"+row[0]+"',\'" +row[1]+ "\',\'" +row[2]+ "\',\'" +row[3]+ "\',\'" +row[4]+ "\',\'" +row[5]+ "\',\'" +row[6]+ "\',\'" +row[7]+ "\',\'" +row[8]+ "\',\'" +row[9]+ "\')" 
                #print('insert_sql = '+insert_sql)  
                self.conn.execute(insert_sql)
                
            except:
                pass
        self.conn.commit()   
        self.conn.close()
        
    def query_user_info(self):
        self.connect()
        select_sql = "SELECT  name, avatarUrl, link, headline, location, business, education, description  FROM zhihu_user_info"
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        user_infos = []
        for row in cursor:
            user_infos.append(row)
        self.conn.close()
        
        return user_infos 
    
    def get_fullname_avatar(self):
        self.connect()
        select_sql = "SELECT u.name, u.avatarUrl, u.headline  FROM zhihu_user_info u WHERE headline <> '' AND NOT EXISTS(SELECT 'x' FROM account a WHERE a.avatarUrl = u.avatarUrl)"
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
        user_infos = []
        for row in cursor:
            user_infos.append(row)
        self.conn.close()
        
        i = random.randint(0, len(user_infos) - 1)
        
        return user_infos[i][0], user_infos[i][1]   
    
    def get_headline(self, avatarUrl):
        self.connect()
        select_sql = "SELECT  u.headline  FROM zhihu_user_info u WHERE avatarUrl = '"+avatarUrl+"'"
        #print('select_sql = '+select_sql)
        cursor = self.conn.execute(select_sql)
       
        headline = ' '
        for row in cursor:
            headline = row[0]
        self.conn.close()
        return headline
    
     
                
if __name__ == '__main__':
    
    sqlUtil = SqlUtil()
    #sqlUtil.drop_account_table()
    #name, avatarUrl = sqlUtil.get_fullname_avatar()
    
    #print('name = '+name)
    #print('avatarUrl = '+avatarUrl)
    #current_count = sqlUtil.get_task_current_count('123')
    #print('current_count = '+ current_count)
    #print('password = '+ account[2])
    
    #sqlUtil.create_zhihu_user_info_table()
    #sqlUtil.insert_zhihu_user_info()
    
    
    #sqlUtil.insert_history('https://www.zhihu.com/question/55761843/answer/181595645', '17065382153', '正常')
    
    #fullname, avatarUrl, headline =  sqlUtil.get_fullname_avatar()
    #print('fullname = '+fullname)
    #print('avatarUrl = '+avatarUrl)
    #print('headline = '+headline)
    #headline = sqlUtil.get_headline('https://pic1.zhimg.com/db1cc506845369c27761eec0c3d21294_is.jpg')
    #print('headline = '+headline)
    '''
    user_infos = sqlUtil.query_user_info()
   
    for user_info in user_infos:
        print('name = '+user_info[0])
        print('avatarUrl = '+user_info[1])
        print('link = '+user_info[2])
        print('headline = '+user_info[3])
       
    '''
    task = sqlUtil.get_pending_task()
    if task == None:
        print('None')
    else:
        print('taskUrl = '+str(task[2]))