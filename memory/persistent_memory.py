import redis
import json

try:
    # try connecting once
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.ping()
    REDIS_AVAILABLE = True
    print("Redis connected")
except:
    # fallback if Redis not running
    REDIS_AVAILABLE = False
    print("Redis not available, using fallback")


def get_user_memory(user_id):
    if not REDIS_AVAILABLE:
        return {}

    try:
        data = r.get(user_id)
        if data:
            return json.loads(data)
    except:
        return {}

    return {}


def update_user_memory(user_id, new_data):
    if not REDIS_AVAILABLE:
        return

    try:
        existing = get_user_memory(user_id)
        existing.update(new_data)

        r.set(user_id, json.dumps(existing))
    except:
        pass