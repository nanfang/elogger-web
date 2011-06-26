from __future__ import unicode_literals, print_function, division
from elogger.database import redis

TOP_NUM = 10
COMING_NUM = 10

class Todo(object):
    def __init__(self, id, title, score, user):
        self.id = id
        self.title = title
        self.score = score
        self.user = user

    def save(self):
        redis.zadd(_ranking_key(self.user), self.id, self.score)
        redis.hset(_title_key(self.user), self.id, self.title)
        return self

    def is_in_tops(self):
        return self.rank() < TOP_NUM

    def rank(self):
        return redis.zrevrank(_ranking_key(self.user), self.id)

def new_todo(user, title):
    return Todo(_next_id(user), title, _score_new_todo(user), user)

def tops(user):
    return [{'id':id, 't':redis.hget(_title_key(user), id), 's':score} for id,score in  _top(user, TOP_NUM)]

def comings(user):
    todo_count = _count(user)
    if todo_count <=TOP_NUM:
        return []
    comings_num=todo_count - TOP_NUM if todo_count < TOP_NUM +COMING_NUM else COMING_NUM
    return [{'id':id, 't':redis.hget(_title_key(user), id), 's':score}
            for id,score in redis.zrevrange(_ranking_key(user), TOP_NUM, TOP_NUM + comings_num, True)]


def count(user):
    return _count(user)

def _score_new_todo(user):
    todo_count = _count(user)
    print(todo_count)
    if not todo_count:
        return TOP_NUM
    if todo_count <= TOP_NUM:
        last_top_id, last_top_score = redis.zrevrange(_ranking_key(user), todo_count - 1, todo_count - 1, True)[0]
        return last_top_score - 1
    crevice = redis.zrevrange(_ranking_key(user), TOP_NUM - 1, TOP_NUM, True)
    last_top_id, last_top_score = crevice[0]
    first_coming_id, first_coming_score = crevice[1]
    score = last_top_score - 1
    if score == first_coming_score:
        for id,score in _top(user, TOP_NUM):
            redis.zincr(_ranking_key(user), id)
        score = last_top_score
    return score

_ranking_key = lambda user: '%s:todos:ranking' % user
_id_key = lambda user: '%s:todos:id' % user
_title_key = lambda user: '%s:todos:title' % user
_next_id = lambda user: int(redis.incr(_id_key(user)))
_top = lambda user, n: redis.zrevrange(_ranking_key(user), 0, n-1, True)
_count = lambda user: redis.zcard(_ranking_key(user))

if __name__ == '__main__':
    print(_count('nanfang'))
    print(tops('nanfang'))
    print(comings('nanfang'))
    print(_score_new_todo('nanfang'))


    