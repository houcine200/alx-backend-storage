#!/usr/bin/env python3
"""A script to  Writing strings to Redis"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for decorated function"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """Wraps called method and tracks
        its passed arguments by storing them in Redis"""
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output

    return wrapper


def replay(fn: Callable) -> None:
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """A class for storing data in Redis with randomly generated keys"""

    def __init__(self):
        """Initialize a Redis client and flush the Redis database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis using randomly generated key and return it"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None) -> Union[str,
                                          bytes,
                                          int,
                                          float]:
        """Convert data back to desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve string data from Redis"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Retrieve integer data from Redis"""
        value = self._redis.get(key)
        if value is not None:
            return int(value.decode("utf-8"))
        return None
