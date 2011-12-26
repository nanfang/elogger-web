import json
from elogger.database import redis


"""
say good bye to v1.0, we are starting v2.0
but we need to get the data.
"""

if __name__ == '__main__':
    data = {}
    for key in redis.keys('*:event-log:*'):
        data[key]=redis.hgetall(key)

    open('data.json').write(json.dumps(data))