from utils import log
import json
import time


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def load(cls, d):
        """
        从保存的字典中生成对象。
        """
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.load(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        k, v = [i for i in kwargs.items()][0]
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        k, v = [i for i in kwargs.items()][0]
        models = []
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                models.append(m)
        return models

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    def save(self):
        models = self.all()
        # 如果没有id, 说明是新添加的元素
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1
                self.id = 1
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    models[index] = self
                    break
            else:
                models.append(self)

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def delete(self):
        models = self.all()
        for i, m in enumerate(models):
            if self.id == m.id:
                index = i
                break
        del models[index]
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{}\n>'.format(classname, s)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


# 定义一个 class 用于保存 message
class Message(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.author = form.get('author', '')
        self.message = form.get('message', '')

    def __repr__(self):
        return '{}: {}'.format(self.author, self.message)


class Weibo(Model):
    def __init__(self, form):
        # id 是独一无二的数据
        # 每个 model 都有自己的 id
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # int(time.time()) 得到一个unixtime
        # unixtime 是现在通用的时间标准
        # 它表示的是从 1970.1.1 到现在过去的秒数
        # 因为1970年是 unix 操作系统创造的时间
        self.created_time = time.ctime(int(time.time()))
        # 我们用 user_id 来标识这个微博是谁发的
        # 初始化为 None
        self.user_id = form.get('user_id', None)


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.created_time = time.ctime(time.time())
        self.content = form.get('content', '')
        self.complete = False

    def status(self):
        return '完成' if self.complete else '待办'