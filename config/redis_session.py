from config.redisconfig import get_redis
import json

class RedisSession:
    def __init__(self):
        self.redis_client = get_redis()

    def set_session(self, session_key: str, data: dict):
        json_data = json.dumps(data)  # Convert dictionary to JSON string
        self.redis_client.set(session_key, json_data)

    def get_session(self, session_key: str):
        data = self.redis_client.get(session_key)
        return json.loads(data) if data else None  # Convert JSON back to dictionary

    def delete_session(self, session_key: str):
        data = self.redis_client.delete(session_key)
        return True
    
    def delete_all_session(self, prefix_pattern: str):
        pattern = f"{prefix_pattern}:*"
        for key in self.redis_client.scan_iter(match=pattern):
            self.redis_client.delete(key)
        return True

redisSessionObj = RedisSession()


"""
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def blacklist_token(jwt_token: str):
    redis_client.setex(jwt_token, 3600, "blacklisted")  # Expires in 1 hour

def is_token_blacklisted(jwt_token: str):
    return redis_client.exists(jwt_token)


"""