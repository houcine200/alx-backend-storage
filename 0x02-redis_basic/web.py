#!/usr/bin/env python3
"""Caching request module"""


import redis
import requests
import time
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        key_count = "count:" + url
        html_content = method(url)

        # Increment access count
        r.incr(key_count)
        # Manually return "OK" after incrementing the access count
        r.incr(key_count)
        # Set cache with expiration time
        r.setex(key, 10, html_content)

        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
    time.sleep(11)  # Wait for cache to expire
