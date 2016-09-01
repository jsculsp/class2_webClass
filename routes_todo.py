from models import Todo

from response import session
from response import template
from response import response_with_headers
from response import redirect
from response import error

from utils import log


def route_index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    todos = Todo.all()


    def todo_tag(t):
        status = t.status()
        return '<p>{} {}@{} 状态: {} <a href="/todo/complete?id={}">完成</a></p>'.format(
            t.id,
            t.content,
            t.created_time,
            status,
            t.id
        )

    todo_html = '\n    <br>\n    '.join([todo_tag(w) for w in todos])
    body = template('todo_index.html', todos=todo_html)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_add(request):
    form = request.form()
    o = Todo(form)
    o.save()
    return redirect('/todo')


def route_complete(request):
    id = int(request.query.get('id', -1))
    o = Todo.find(id)
    o.complete = not o.complete
    o.save()
    return redirect('/todo')


route_dict = {
    '/todo': route_index,
    '/todo/add': route_add,
    '/todo/complete': route_complete,
}
