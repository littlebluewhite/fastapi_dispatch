import os

Dispatch_Redis_config = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": "1"
}

Dispatch_Database = {
    "host": "127.0.0.1",
    "port": 3306,
    "db": "dispatch",
    "user": "root",
    "password": "123456"
}

Test_Database = {
    "host": "127.0.0.1",
    "port": 3306,
    "db": "test2",
    "user": "root",
    "password": "123456"
}


def dispatch_config():
    result = {
        "Dispatch_Redis_config": Dispatch_Redis_config,
        "Dispatch_Database": Dispatch_Database,
        "Test_Database": Test_Database,
    }
    runtime_path = "/".join(os.path.abspath(__file__).replace("\\", "/").split("/")[0:-5])\
                   + "/runtime/server/config/host_configs.py"
    if os.path.exists(runtime_path):
        # result.update()
        pass
    return result


if __name__ == "__main__":
    print(dispatch_config())
