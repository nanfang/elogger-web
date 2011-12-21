from redis import Redis

class RedisCache(Redis):
    def hgetall(self, name):
        result = super(RedisCache, self).hgetall(name)
        if result:
            for k, v in result.iteritems():
                result[k] = v.decode('utf-8')
        return result

    def get(self, key):
        result = super(RedisCache, self).get(key)
        if result:
            result=result.decode('utf-8')
        return result

cache = RedisCache()
