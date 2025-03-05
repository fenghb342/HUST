import re    # 正则表达式，用于匹配字符
from urllib import request
import requests
import time
import random
import os
import json


log_file_path = 'log.txt'

'''
config格式
header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            
            "Content-Length": "979",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_SERVER=; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_DOMAIN=; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_COOKIE_USERNAME=M202471575; EPORTAL_COOKIE_NEWV=true; EPORTAL_COOKIE_PASSWORD=85fbd517619db7e66b5aaa30ee4fc6b6b35a9afcdc9d7529481c772548a6444f8579ab42e2beec766db05c1178afec0edd9fb1ad94891a02574bb2462434f9a8a618d4d604f9feff50ded47c7c293f85151765af0dec2174ac217babf7531b468079934e9702114f32f265fe8877bab92ae07f4d726180c767dc72fa0651e146; EPORTAL_COOKIE_SERVER_NAME=; EPORTAL_USER_GROUP=null; JSESSIONID=1E6FF2BE760522C6A3812D57B57E1CFF; JSESSIONID=E0BFBEE60CB68347887C16F3ED81C239",
            "Host": "172.18.18.61:8080",
            "Origin": "",
            "Referer": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        }
        # 设置post的请求数据，浏览器点击F12，在Netword中选中post请求，点击payload面板中查看
data = {
        "userId": '',  # 校园网账号
        "password": '',
        "passwordEncrypt": 'true',
        "operatorPwd": '',
        "operatorUserId": '',
        "validcode": '',#验证码
        "service": '',
}'''
'''
# 第一个post请求的URL
post_URL = ''
# 第二个get请求的URL（浏览器可访问的url）
get_URL = ''

'''


    
def  gettime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def gettime_print(data, data2=None, data3=None):
    if data2 is None and data3 is None:
        print(f"{gettime():<30}{data}\n")
    elif data3 is None:
        print(f"{gettime():<30}{data}{data2}\n")
    else:
        print(f"{gettime():<30}{data}{data2}{data3}\n")

    

def get_title(get_URL,html):
    # 获取tittle元素内容
    res = re.findall('<title>(.*)</title>', html.decode(encoding="GBK", errors="strict"))
    #gettime_print('res:', res)
    title = ''
    if len(res) == 0:
        gettime_print("未连接校园网访问",get_URL,"失败，或请检查get_URL地址！")
        pass
    else:
        title = res[0]
        #gettime_print(f"title: {title} ")
    return title


def login_success(get_URL):
    # 请求校园网url
    response = request.urlopen(get_URL)
    html = response.read()
    # 获取tittle元素内容
    title = get_title(get_URL,html)

    # 根据title元素内容判断是否处于已登录状态
    if title == '登录成功':    
        gettime_print(f'{'当前状态为：已登录成功！'}')
        
        return True
    else:
        gettime_print(f'{'当前状态为：未登录！'}')
        time.sleep(2)
        return False


def login(get_URL,post_URL, data, header):
    # 设置post的请求头，浏览器点击F12，在Netword中选中post请求，点击Headers、request header面板中查看
    t= 10.0
    # 发送post请求（设置好header和data）
    gettime_print(f"{'发送post请求（务必设置好header和data）...'}")
    time.sleep(1)
    response = requests.post(post_URL, data, headers=header)
    uft_str = response.text.encode("iso-8859-1").decode('utf-8')
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{gettime():<30}状态码: {response}\n")
    open(log_file_path).close()
    gettime_print(f"{'post请求状态码:'}{format(response)}")  # 打印状态码
    time.sleep(3)
    # 发送get请求，登录校园网
    gettime_print(f"{'发送get请求...'}")  
    schoolWebLoginURL = get_URL
    response = requests.get(schoolWebLoginURL).status_code  # 直接利用 GET 方式请求这个 URL 同时获取状态码
    gettime_print(f"{'get请求状态码:'}  {format(response)}")  # 打印状态码
    if response == 200:
        gettime_print(f"{'登录成功！'}  ")
        return True
    else:
        gettime_print(f"{'登录失败！'}   ")
        gettime_print(f"{'请检查config文件的header和data！'}")
        time.sleep(30)
        return False










def main():
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{gettime():<30}{'自动联网脚本开始运行...'}\n") 
    gettime_print(f"{'自动联网脚本开始运行...'}")
    time.sleep(1)    
    # 从文件中读取配置
    gettime_print(f"当前工作目录: {os.getcwd()}")
    file_path = 'config.json'
    time.sleep(1)
    if not os.path.exists(file_path):
        gettime_print(f"文件不存在: {file_path}")
        time.sleep(10)
    else:
        # 从文件中读取配置
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        header = config['header']
        data = config['data']
        urls = config['urls']
        post_URL = urls['post_URL']
        get_URL = urls['get_URL']
        # 打印header和data以确保读取正确
        gettime_print(f"header: {header}\n")
        gettime_print(f"data: {data}\n")

    #/ 设置日志文件路径
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{gettime():<30}{'post_URL'}{post_URL}\n")
        gettime_print(f"{'post_URL:'}{post_URL:<60}")
        log_file.write(f"{gettime():<30}{'get_URL:'} {get_URL}\n")  
        gettime_print(f"{'get_URL:'}{get_URL}")
    open(log_file_path).close()
    while True:    
        hadlogin = login_success(get_URL)
        if not hadlogin:
            t= 5.0
            gettime_print(f'{'需要登录，正在登录...'}')
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{gettime():<30}{'需要登录，正在登录...'}\n ")
            open(log_file_path).close()
            time.sleep(3)
            if login(get_URL,post_URL, data, header):  # 传递post_URL、data和header参数
                t= 1.0
        else:
            t= 600.0
            #gettime_print(f'已登录  ')
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{gettime():<30}当前状态为: {'已登录成功' if hadlogin == True else False}\n")  
            open(log_file_path).close()
        # 检查文件大小，如果大于100000KB则清空文件
        if os.path.getsize(log_file_path) > 102400000:
            open(log_file_path, 'w').close()

        # 每10min左右检测一次是否成功连接
        rand = random.uniform(0, 10)
        gettime_print(int(t + rand),f"{'s后再次验证连接状态...'}")
        time.sleep(t + rand)
        #time.sleep(100 + rand)
if __name__ == '__main__':
    main()
