#!/usr/bin/env python3
"""A script to get the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """returns the list of school having a specific topic"""
    result = mongo_collection.find({"topic": topic})
    return list(result)
