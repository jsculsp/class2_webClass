class Movie(object):
    def __init__(self):
        self.num = ''
        self.name = ''
        self.score = ''
        self.people_num = ''
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
        m.score = i.split('<span class="rating_num" property="v:average">')[1].split('</span>')
        m.people_num = i.split('<span>')[1].split('</span>')[0]
        if '<span class="inq">' in i:
            m.quote = i.split('<span class="inq">')[1].split('</span>')[0]
        lst.append(m)
    return lst