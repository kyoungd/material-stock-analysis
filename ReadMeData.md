# STREAMING DATA (REAL TIME)

## 1. bar

{ 'close': 46.09,
'high': 46.1199,
'low': 46.09,
'open': 46.095,
'symbol': 'UBER',
'timestamp': 1627493640000000000,
'trade_count': 101,
'volume': 9629,
'vwap': 46.10465}

## publish stream

redisPublisher.publish(bar)

## subscription stream

redisSubscriber(callback=RealTimeBar.redis_add_bar).work(bar)

# ANALYSIS EVENT (Every 5 seconds)

redis3barCandidates
