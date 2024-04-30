#!/usr/bin/env python3
"""
Python script that provides some stats
about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")

    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    count_get_status = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(count_get_status))

    # Aggregation pipeline to get top 10 IPs
    top_ips_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = collection.aggregate(top_ips_pipeline)

    print("IPs:")
    for ip_data in top_ips:
        print("\t{}: {}".format(ip_data["_id"], ip_data["count"]))
