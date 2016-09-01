from models import Message
from models import User
from utils import log
from models import Weibo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error


import random

message_list = []


def random_str():
    seed = 'aalkdfjwrgssdfgsdfgsdfvxcrtewydfghdlvzkxclvjlaskdfasdzcxvasdrwe'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    username = current_user(request)
    body = template('index.html',
                    username=username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169',
    }
    # log('login, headers', request.headers)
    log('login, cookies ({})'.format(request.cookies))
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        log('debug form ({})'.format(form))
        u = User(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登陆成功'
            username = u.username
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = template('login.html',
                    result=result,
                    username=username, )
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.x 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或密码长度必须大于2'
    else:
        result = ''
    body = template('register.html',
                    result=result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    """
    主页的处理函数, 返回主页的响应
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169',
        # 'Location': ''
    }
    # log('本次请求的 method', request.method)
    header = response_with_headers(headers)
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        msg.save()
        message_list.append(msg)
        # 应该在这里保存 message_list
    msgs = '<br>'.join([str(m) for m in message_list])
    body = template('html_basic.html',
                    messages=msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_profile(request):
    """
    如果登录了, 则返回一个页面显示用户的
    三项资料(id, username, note)
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169',
        # 'Location': ''
    }
    username = current_user(request)
    header = response_with_headers(headers)
    user = User.find_by(username=username)
    body = template('profile.html',
                    id=user.id,
                    username=user.username,
                    note=user.note)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

    pass


# 定义一个函数统一检测是否登录
def login_required(route_function):
    def func(request):
        username = current_user(request)
        if username == '游客':
            # 没登陆 不让看 重定向到 /login
            return redirect('/login')
        return route_function(request)

    return func


def route_blog(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    body = template('starbuzz/blog.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/messages': login_required(route_message),
    '/login': route_login,
    '/register': route_register,
    '/profile': login_required(route_profile),
    # '/weibo': route_weibo_index,
    # '/weibo/new': login_required(route_weibo_new),
    # '/weibo/add': login_required(route_weibo_add),
    # '/weibo/delete': login_required(route_weibo_delete),
    # '/blog': route_blog,
}