from dispatch_data import reply_data


def ccc(data):
    print(type(data))
    print(data.redis_tables)


if __name__ == "__main__":
    ccc(reply_data)
