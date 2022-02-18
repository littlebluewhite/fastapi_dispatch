import redis
from dispatch_config import dispatch_config

redis_config = dispatch_config()["Dispatch_Redis_config"]

pool = redis.ConnectionPool(host=redis_config["host"],
                            port=redis_config["port"],
                            db=redis_config["db"])
redisDB = redis.Redis(connection_pool=pool)

if __name__ == "__main__":
    pass
