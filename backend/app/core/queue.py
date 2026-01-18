"""Redis Queue configuration for background tasks"""
import os
import redis
from rq import Queue
from app.core.config import settings

# Redis connection
conn = redis.from_url(settings.REDIS_URL)

# Default queue
q = Queue(settings.RQ_QUEUE_NAME, connection=conn)
