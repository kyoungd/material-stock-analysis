import redis
from redisUtil import KeyName, RedisAccess


class RedisSortedSet:

    def __init__(self, key, r: redis = None, callback=None):
        self.redis = RedisAccess.connection(r)
        self.key = key
        self.callback = callback

    @property
    def get_key(self):
        return self.key

    def _getAll(self, key, low, high):
        return self.redis.zrevrangebyscore(key, high, low, withscores=True)

    def getAll(self, low, high):
        return self._getAll(self.key, low, high)

    def _set(self, key, name, value):
        self.redis.zadd(key, {name: value})

    def set(self, name, value):
        self._set(self.key, name, value)

    def killme(self):
        self.redis.delete(self.key)


class LatestPrices(RedisSortedSet):
    def __init__(self, r=None, callback=None):
        lastPriceKey = "LASTPRICE"
        RedisSortedSet.__init__(self, lastPriceKey, r, callback)

    def getAll(self, low=3, high=20):
        return RedisSortedSet.getAll(self, low, high)


class ThreeBarPlayScore(RedisSortedSet):
    def __init__(self, r=None, callback=None):
        lastPriceKey = KeyName.KEY_THREEBARSCORE
        RedisSortedSet.__init__(self, lastPriceKey, r, callback)

    def getAll(self, low=0, high=100):
        return RedisSortedSet.getAll(self, low, high)


if __name__ == "__main__":
    app = ThreeBarPlayScore()
    app.killme()
    app.set("young", 60)
    app.set("john", 55)
    app.set("orion", 50)
    scores = app.getAll()
    print(scores)
