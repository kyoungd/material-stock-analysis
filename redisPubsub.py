import threading
import redis
import json
from redisTSBars import RealTimeBars
from redisUtil import KeyName
from redisSortedSet import ThreeBarPlayScore


class RedisSubscriber(threading.Thread):
    def __init__(self, channels, r=None, callback=None):
        threading.Thread.__init__(self)
        if (r == None):
            self.redis = redis.StrictRedis(
                host='127.0.0.1', port=6379, db=0)
        else:
            self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels.value)
        self.callback = callback

    def get_redis(self):
        return self.redis

    def work(self, package):
        if (self.callback == None):
            print(package['channel'], ":", package['data'])
        else:
            if (type(package) is 'str'):
                data = json.load(package)
            else:
                data = package
            self.callback(data)

    def run(self):
        for package in self.pubsub.listen():
            if package['data'] == "KILL":
                self.pubsub.unsubscribe()
                print("unsubscribed and finished")
                break
            else:
                self.work(package)


class RedisPublisher:
    def __init__(self, channels, r=None):
        if (r == None):
            self.redis = redis.StrictRedis(
                host='127.0.0.1', port=6379, db=0)
        else:
            self.redis = r
        self.channels = channels

    def publish(self, data):
        package = json.dumps(data)
        self.redis.publish(self.channels.value[0], package)

    def killme(self):
        self.redis.publish(self.channels[0], 'KILL')


class StreamBarsSubscriber(RedisSubscriber):
    def __init__(self):
        self.rtb = RealTimeBars()
        RedisSubscriber.__init__(self,
                                 KeyName.EVENT_BAR2DB, callback=self.rtb.redis_add_bar)


class StreamBarsPublisher(RedisPublisher):
    def __init__(self):
        RedisPublisher.__init__(self, KeyName.EVENT_BAR2DB)


class ThreeBarScoreSubscriber(RedisSubscriber):
    def __init__(self):
        self.score = ThreeBarPlayScore()
        RedisSubscriber.__init__(self,
                                 KeyName.EVENT_BAR2DB, callback=self.score.subscribe)


if __name__ == "__main__":
    pass
