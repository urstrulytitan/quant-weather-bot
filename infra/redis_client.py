import os
import redis.asyncio as redis

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis = redis.from_url(redis_url)