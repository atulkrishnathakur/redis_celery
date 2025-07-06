from config.redisconfig import get_redis
import json

class RedisSession:
    def __init__(self):
        self.redis_client = get_redis()

    def set_session(self, prefix: str, session_key: str, data: dict):
        # Here prefix must be unique. like user id
        json_data = json.dumps(data)  # Convert dictionary to JSON string
        self.redis_client.set(f"{prefix}:{session_key}", json_data)

    def get_session(self, prefix: str, session_key: str):
        data = self.redis_client.get(f"{prefix}:{session_key}")
        return json.loads(data) if data else None  # Convert JSON back to dictionary

    def delete_session(self, prefix: str, session_key: str):
        data = self.redis_client.delete(session_key)
        return True
    
    def delete_all_session(self, prefix: str):
        pattern = f"{prefix}:*"
        for key in self.redis_client.scan_iter(match=pattern):
            self.redis_client.delete(key)
        return True

redisSessionObj = RedisSession()