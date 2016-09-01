# 2016/8/12
#
# ========
# 作业 (会更新)
#
# 注意, 作业会在这里更新, 对作业有问题请评论
# 注意, 登录论坛后才有评论功能
# ========
# 更新 2.4
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    query_list = []
    for k, v in query.items():
        kv = str(k) + '=' + str(v)
        query_list.append(kv)
    query_format = '&'.join(query_list)
    path_and_query = '?'.join([path, query_format])
    return path_and_query


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典
def get(url, query={}):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)
    path = path_with_query(path, query)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    lst = []
    for k, v in headers.items():
        kv = str(k) + ': ' + str(v)
        kv += '\r\n'
        lst.append(kv)
    header_format = ''.join(lst)
    return header_format


# 作业 2.4
#
# 为作业 2.3 写测试
def test_header_from_dict():
    headers = {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    expected = [
        'Content-Type: text/html\r\nContent-Length: 127\r\n',
        'Content-Length: 127\r\nContent-Type: text/html\r\n',
    ]

    assert header_from_dict(headers) in expected


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""


class Movie(object):
    def __init__(self):
        self.num = ''
        self.name = ''
        self.score = ''
        self.rating = ''
        self.quote = ''

    def __repr__(self):
        return '{0.num} {0.name} {0.score} {0.rating} {0.quote}'.format(self)


def parse_body(body):
    body = body.split('<ol class="grid_view">')[1].split('</ol>')[0]
    div_list = body.split('<div class="item">')[1:]
    lst = []
    for i in div_list:
        m = Movie()
        m.num = i.split('<em class="">')[1].split('</em>')[0]
        m.name = i.split('<span class="title">')[1].split('</span>')[0]
        m.score = i.split(' <span class="rating_num" property="v:average">')[1].split('</span>')[0]
        m.eva_num = i.split('<span>')[1].split('</span>')[0]
        if '<span class="inq">' in i:
            m.quote = i.split('<span class="inq">')[1].split('</span>')[0]
        lst.append(m)
    return lst


lst = parse_body(body)
for i in lst:
    print('{0.num}  {0.name: <14}   {0.score}       {0.eva_num}     {0.quote}'.format(i))

# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""


def get_all(url):
    lst = []
    query = {
        'start': 0,
    }
    while query['start'] < 250:
        status_code, headers, body = get(url, query)
        lst += parse_body(body)
        query['start'] += 25
    return lst


def main():
    url = 'https://movie.douban.com/top250'
    l = get_all(url)
    for i in l:
        log(i)


if __name__ == '__main__':
    main()
