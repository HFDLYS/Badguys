import requests
from bs4 import BeautifulSoup
import json
import constants
import PIL.Image as Image
import re

def login(username, password):
    payload = {
        'loginname': username,
        'password': password,
        'csrfmiddlewaretoken': '',
        'next': ''
    }
    session = requests.Session()
    session.headers = constants.HEADERS
    content = session.get(constants.LOGIN_URL).text
    soup = BeautifulSoup(content, 'html.parser')
    payload['csrfmiddlewaretoken'] = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
    
    session.post(constants.LOGIN_URL, data=payload)
    return session.cookies.get_dict()
    
    

def get_captcha(cookie):
    content = requests.get(constants.CAPTCHA_URL, cookies=cookie, headers= constants.HEADERS).content

    temp = json.loads(content.decode('utf-8'))
    hash = temp['key']
    url = 'https://aa.bjtu.edu.cn/captcha/image/' + hash + '/'
    content = requests.get(url, cookies=cookie, headers=constants.HEADERS).content
    path = 'dataset/' + hash + '.png'
    with open(path, 'wb') as f:
        f.write(content)
    Image.open(path).show()
    return hash

def get_course(cookie, keyword, type = 'school'):
    #type = 'school' or 'cross' or 'others'
    url = constants.COURSE_URL.format('',type)
    content = requests.get(url, cookies=cookie, headers= constants.HEADERS).content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')
    if not table:
        print('未找到课程表！')
        return -1
    data = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if not cols:
            continue
        cols = cols[0:3]
        if cols[0].input:
            cols[0] = cols[0].input['value']
        else:
            continue
        cols = [temp for temp in cols]
        
        for i in keyword:
            if i in cols[2].text:
                data.append(cols[0])
    return data

def get_captcha_dataset(cookie):
    content = requests.get(constants.CAPTCHA_URL, cookies=cookie, headers= constants.HEADERS).content

    temp = json.loads(content.decode('utf-8'))
    hash = temp['key']
    url = 'https://aa.bjtu.edu.cn/captcha/image/' + hash + '/'
    content = requests.get(url, cookies=cookie, headers=constants.HEADERS).content
    with open('dataset/' + hash + '.png', 'wb') as f:
        f.write(content)
    return hash

def message_analysis(cookie, message):
    _cookie = cookie.copy()
    _cookie['messages'] = message
    content = requests.get(constants.ANALYSIS_URL, cookies=_cookie, headers=constants.HEADERS).content
    t = re.search(r'message \+= "(.*?)<br/>";', str(content), re.M|re.I)
    t = t.group(1)
    t = t.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
    return t

def submit_course(cookie, hash, answer, course):    
    checkboxs = ''
    for i in course:
        checkboxs += i + ','
    checkboxs = checkboxs[:-1]
    payload = {
        'checkboxs': checkboxs,
        #'is_cross': is_cross,
        'hashkey': hash,
        'answer': answer,
    }

    res = requests.post(constants.POST_URL, data=payload, cookies=cookie, headers=constants.HEADERS, allow_redirects=False)
    res = eval(str(res.headers))
    resurt = res['Set-Cookie']
    print(resurt)
    if 'message' in resurt:
        t = re.search('messages=(.*?);', resurt)
        print(t.group(1))
        return t.group(1) 
    else:
        print('部分（或全部）选课失败！或验证码错误🤔我不知道喵')
        raise Exception

def delete_course(cookie, course):
    
    payload = {
        'select_id': course,
    }
    res = requests.post(constants.DELETE_URL, data=payload, cookies=cookie, headers=constants.HEADERS, allow_redirects=False)
    res = eval(str(res.headers))
    resurt = res['Set-Cookie']
    print(resurt)
    if 'message' in resurt:
        t = re.search('messages=(.*?);', resurt)
        return t.group(1) 
    else:
        print('部分（或全部）退课失败！我不知道喵')
        raise Exception
    