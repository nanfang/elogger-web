from __future__ import unicode_literals, print_function, division
from redis import Redis

class MyRedis(Redis):
    def hgetall(self, name):
        result = super(MyRedis, self).hgetall(name)
        if result:
            for k, v in result.iteritems():
                result[k] = v.decode('utf-8')
        return result

redis = MyRedis()
