#!/usr/bin/env python3
"""Caching request module"""


import redis
import requests
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
        access_count = r.get(key_count)
        if not access_count:
            r.set(key_count, 1)
        else:
            r.incr(key_count)
        html_content = method(url)

        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
