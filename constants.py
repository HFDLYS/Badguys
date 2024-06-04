LOGIN_URL = 'https://aa.bjtu.edu.cn/client/login/'
CAPTCHA_URL = 'https://aa.bjtu.edu.cn/captcha/refresh/'
POST_URL = 'https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=submit'
COURSE_URL = 'https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?zxjxjhh=&kch={}&action=load&iframe={}&submit=+%E6%9F%A5+%E8%AF%A2+&has_advance_query=&page=1&perpage=8000'
ANALYSIS_URL = 'https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/'
DELETE_URL = 'https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?action=delete'

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/',
        'Host': 'aa.bjtu.edu.cn',
        'Origin': 'https://aa.bjtu.edu.cn',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        }

RETRY = 10
