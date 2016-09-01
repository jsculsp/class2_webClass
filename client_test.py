import ssl
import socket


def parsed_url(url):
    """
    解析 url 返回（protocol， host, port, path）
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # 检查默认path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = h[1]

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.receive(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把 response 解析出 status_code, headers, body 返回
    状态码是 int
    headers 是 dict
    body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(':')
        headers[k] = v
    return status_code, headers, body


def get(url):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)

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


def main():
    url = 'http://movie.douban.com/top250'
    status_code, header, body = get(url)
    lst = parse_body(body)
    return lst
