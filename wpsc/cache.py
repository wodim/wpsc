import redis

redis_prefix = 'wpstore-checker'
redis = redis.StrictRedis('127.0.0.1', '6379', decode_responses=True)

redis_key = lambda k: '%s.%s' % (redis_prefix, k)