# -*- coding: utf-8 -*-
import csv
import requests

session = requests.session()
# example 1 读取 csv 返回列表
def read_csv(fn='data1.csv'):
    
    with open(fn, encoding="utf-8") as fr:
        csvfr = csv.reader(fr)
        rows = [row for row in csvfr]
    return rows


# example 2 读取 csv 返回列表
def read_csv_dict(fn="data2.csv"):
    """
    data2.csv 的数据格式，
    读取返回字典比较容易处理
    """
    with open(fn, encoding="utf-8") as fr:
        dict_rows = csv.DictReader(fr, fieldnames=None)
        # 不指定 fieldnames 的情况下
        # 默认第一行数据作为 fieldnames
        for row in dict_rows:
            print(row)  # row 是一个字典
            




def download_avatar(full_name, avatar_url):
    print('full_name= '+full_name)  
    print('avatar_url = '+avatar_url) 
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    r = session.get(avatar_url, headers=headers, verify = False)
    with open('./avatars/'+full_name+'.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    
if __name__ == '__main__':
    '''
    rows = read_csv('./data/zhihu_user_info.csv')
    print('len(rows) = '+str(len(rows)))
    
    del rows[0]
    for row in rows:
        save_avatar(row[0], row[1].replace('_is', ''))
        print('row[0] = '+row[0])  
        print('row[1] = '+row[1].replace('_is', ''))     
    '''
    
    
    #save_avatar('miaooooo', 'https://pic1.zhimg.com/61d134d1b8ab5de9145948edb70f1a3c_is.jpg')   
    '''
    avatarUrl = 'https://pic4.zhimg.com/6ba64e97f_is.jpg'
    print('avatarUrl = '+avatarUrl)
    index = avatarUrl.rindex('/')
    avatarName = avatarUrl[index+1:]
    print('index = '+str(index))
    print('avatarName = '+avatarName)
    '''
        
    print('开始')
    i = 0
    while True:
        i += 1
        print('i = '+str(i))
        if i > 10:
            print('break')
            break
            print('break2')
        
    print('退出')
          