from __future__ import unicode_literals, print_function, division
from redis import Redis

class MyRedis(Redis):
    def hgetall(self, name):
        result = super(MyRedis, self).hgetall(name)
        if result:
            for k, v in result.iteritems():
                result[k] = v.decode('utf-8')
        return result

    def get(self, key):
        result = super(MyRedis, self).get(key)
        if result:
            result=result.decode('utf-8')
        return result
redis = MyRedis()
