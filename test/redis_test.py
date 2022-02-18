import json

from dispatch_redis.redis import redisDB

if __name__ == "__main__":
    # print(redisDB.hget("dispatch_status", 9))
    # print(redisDB.hvals("dispatch_status"))
    print(type(json.loads(redisDB.hget("dispatch_status_by_name", "pending"))))
