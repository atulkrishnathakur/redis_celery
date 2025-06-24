import redis

# Redis connection function
def get_redis():
    return redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)