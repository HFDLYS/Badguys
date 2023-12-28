import access


def run(cookie = None, hash = None, key = None, course = None):
    if cookie == None:
        log = input('请输入学号：')     #可以直接写上去哦
        pwd = input('请输入密码：')     #23级密码为身份证后六位 
        cookie = access.login(log, pwd)
        if 'sessionid' not in cookie:
            print('登录失败！')
            return -1
    if hash == None or key == None:
        hash = access.get_captcha(cookie)

        print('验证码已保存至.\dataset\\' + hash + '.png')
        print('Hash: ' + hash)
        key = input('请输入验证码：')
        if key == '' or key == None or key[0] == ' ':
            hash = access.get_captcha_dataset(cookie)
            print('验证码已保存至.\dataset\\' + hash + '.png')
            print('Hash: ' + hash)
            key = input('请输入验证码：')
    if course == None:

        course = -1
        while course == -1:
            try:
                course = access.get_course(cookie,  [])

                '''
                格式如下：
                ['A121080B:国际标准舞 03', 'A124012B:声乐演唱基础 01', ]
                (注意课序号和详情中间有“  :  ”)
                全校仍选课只能由三个哦
                '''
            except:
                pass
    if course == []:
        print('蒸🐟🐟，没这课了😭')
    print(cookie, hash, key, course)
    #防止一次失败
    for _ in range(10):
        message = access.post(cookie, hash, key, course)
        if message != -1:
            print(access.message_analysis(cookie, message))
            break


if __name__ == '__main__':
    # 参数样例如下
    # cookie = {'csrftoken': '🐱🐱🐱🐱🐱', 'sessionid': '🐟🐟🐟🐟🐟'}       由login()获取
    # hash = '🐱🐱🐱🐱🐱'       由get_captcha()获取
    # key = '🐟🐟🐟🐟🐟'
    # course = ['000000', '000000', '000000', '000000', '000000', '000000']     #课程号，一般可以通过执行一次get_course()获取
    cookie = None
    hash = None
    key = None
    course = None
    run(cookie, hash, key, course)
