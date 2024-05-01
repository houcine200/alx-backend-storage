#!/usr/bin/env python3
"""A script to  Writing strings to Redis"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """A class for storing data in Redis with randomly generated keys"""
    def __init__(self):
        """Initialize a Redis client and flush the Redis database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis using randomly generated key and return it"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
