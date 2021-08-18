import redis
import json
from redisUtil import KeyName


class RedisHash:

    def __init__(self, key, r=None, callback=None):
        if (r == None):
            self.redis = redis.StrictRedis(
                host='127.0.0.1', port=6379, db=0)
        else:
            self.redis = r
        self.callback = callback
        self.key = key

    @property
    def get_key(self):
        return self.key

    def _getAll(self, key):
        return self.redis.hgetall(key)

    def getAll(self):
        return self._getAll(self.key)

    def _add(self, key, symbol, jsondata):
        data = json.dumps(jsondata)
        self.redis.hset(key, symbol, data)
        if (self.callback != None):
            self.callback(symbol, jsondata)

    def add(self, symbol, jsondata):
        return self._add(self.key, symbol, jsondata)

    def _value(self, key, symbol):
        data = self.redis.hget(key, symbol)
        return json.loads(data)

    def value(self, symbol):
        return self._value(self.key, symbol)


class ThreeBarPlayStack(RedisHash):
    def __init__(self, r=None, callback=None):
        self.key = KeyName.KEY_THREEBARSTACK.value
        RedisHash.__init__(self, self.key, r, callback)


if __name__ == "__main__":
    app = ThreeBarPlayStack()
    app.add("AAPL", {'name': 'test', 'data': 'this is text'})
    print(app.value("AAPL"))
