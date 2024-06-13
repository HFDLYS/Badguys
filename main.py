import spider
import constants

def run(cookie = None, hash = None, key = None, delete = [] ,course = None):
    if cookie == None:
        log = None
        pwd = None
        try:
            with open("account.txt", "r") as f:
                log = f.readline().strip()
                pwd = f.readline().strip()
            if log == '' or pwd == '' or log == None or pwd == None:
                raise Exception
        except:
            log = input('请输入学号：')     #可以直接写上去哦
            pwd = input('请输入密码：')     #23级密码为身份证后六位 
        cookie = spider.login(log, pwd)
        if 'sessionid' not in cookie:
            print('登录失败！')
            return -1
    if delete != None:
        for delete_course in delete:
            retry = constants.RETRY
            message = ''
            while retry > 0:
                try:
                    message = spider.delete_course(cookie, delete_course)
                    break
                except:
                    retry -= 1
            if message != '':
                decode = spider.message_analysis(cookie, message)
                print(decode)
            
    while hash == None or key == None or key == '' or key == " " or (len(key) != 4):  #防止不输入验证码
        hash, content = spider.get_captcha(cookie)
        key = input('请输入验证码：（不输入则重新获取）')
    if course == None:

        
        course_type = 'school'
        #全校乱选课（默认） school
        #本学院其他年级课 cross
        #其他学院专业课 others
        #本学院课程 ？这你都选不到吗


        course_name = []
        '''
        格式如下：
        ['A121080B:国际标准舞 03', 'A124012B:声乐演唱基础 01', ]
        (注意课序号和详情中间有“  :  ”,英文冒号的不是中文冒号！！！)
        全校仍选课只能留三个哦
        '''

        course = -1
        retry = constants.RETRY
        while course == -1 and retry > 0:
            try:
                course = spider.get_course(cookie,  course_name, course_type)
            except:
                pass
            retry -= 1
            print('获取课程失败！重试中...，剩余次数：', retry, '次')
        if course == -1:
            print('获取课程失败！')
            exit()
    if course == []:
        print('蒸🐟🐟，没这课了😭')
    print(cookie, hash, key, course)
    #防止一次失败
    retry = constants.RETRY
    message = ''
    while retry > 0:
        try:
            message = spider.submit_course(cookie, hash, key, course)
            print(message)
            break
        except:
            print('失败！重试中...，剩余次数：', retry - 1, '次')
            retry -= 1
    if message != '':
        decode = spider.message_analysis(cookie, message)
        print(decode)


if __name__ == '__main__':
    # 参数样例如下
    # cookie = {'csrftoken': '🐱🐱🐱🐱🐱', 'sessionid': '🐟🐟🐟🐟🐟'}
    # 不写也行，会自动读取account.txt，或者自己输入
    # hash 和 key 也可以不写，会自动获取
    # hash 是验证码的hash值，key 是观察验证码后输入的值 这个可以提前获取，保证在抢课时旗开得胜，也可以当场获取
    # hash = '🐱🐱🐱🐱🐱'       由get_captcha()获取
    # key = '🐟🐟🐟🐟🐟'        由你的眼睛获取
    # delete = ['000000', '000000', '000000', '000000', '000000', '000000']     #这是你不想要的课，自己去看看课程号是什么
    # course = ['000000', '000000', '000000', '000000', '000000', '000000']     #课程号
    # 如果设置成 None 则可以通过执行一次get_course()获取
    
    op = input('是否提前获取验证码？(y/n)')
    
    cookie = None
    hash = None
    key = None
    delete = []
    course = None
    
    if op == 'y':
        while hash == None or key == None or key == '' or key == " " or (len(key) != 4):
            hash, content = spider.get_captcha(cookie)
            key = input('请输入验证码：（不输入则重新获取）')
    
    run(cookie, hash, key, delete, course)
