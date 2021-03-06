import base64
import json

from fastapi.encoders import jsonable_encoder
from dispatch_exception import DispatchException
from dispatch_redis.redis import redisDB


def clean_redis_by_name(table_name):
    if redisDB.exists(table_name):
        if redisDB.delete(table_name) == 1:
            print(f"clean redis table: {table_name}")


def write_sql_data_to_redis(table_name: str, sql_data_list: list, schemas_model,
                            key: str = "id", update_list: list = None) -> list:
    """

    :param table_name:
    :param sql_data_list:
    :param schemas_model:
    :param key:
    :param update_list: update sql table可以加此參數，減少對redis的訪問，不加也可以
    :return:
    """
    update_dict = dict()
    if update_list is None:
        update_list = list()
    for update_data in update_list:
        update_dict[update_data.id] = update_data
    result = list()
    for sql_data in sql_data_list:
        row = schemas_model(**jsonable_encoder(sql_data, custom_encoder={
            bytes: lambda v: base64.b64encode(v).decode('utf-8')}))
        # 寫入主表
        if key == "id":
            value = row.json()
            redisDB.hset(table_name, getattr(row, key), value)
        # 寫入附表(index table)
        elif not update_list or getattr(update_dict.get(row.id, None), key, None) is not None:
            # sql type 是 json list的情況
            if isinstance(getattr(row, key), list):
                for item in getattr(row, key):
                    value_list = list()
                    original_data = redisDB.hget(table_name, item)
                    if original_data:
                        value_list = json.loads(original_data)
                    redisDB.hset(table_name, item, json.dumps(list(set(value_list+[row.id]))))
            # sql type 是單一值的情況
            else:
                item = getattr(row, key)
                value_list = list()
                original_data = redisDB.hget(table_name, item)
                if original_data:
                    value_list = json.loads(original_data)
                redisDB.hset(table_name, item, json.dumps(list(set(value_list+[row.id]))))
        result.append(row)
    return result


def read_redis_all_data(table_name: str) -> list[dict]:
    result = []
    for datum in redisDB.hvals(table_name):
        result.append(json.loads(datum))
    return result


def read_redis_data(table_name: str, key_set: set) -> list:
    data_list = list()
    for key in key_set:
        data = redisDB.hget(table_name, key)
        if not data:
            raise DispatchException(status_code=404, detail=f"id:{key} is not exist")
        data_list.append(json.loads(data))
    return data_list


def delete_redis_data(table_name: str, data_list: list, schemas_model,
                      key: str = "id", update_list: list = None) -> str:
    """

    :param table_name:
    :param data_list:
    :param schemas_model:
    :param key:
    :param update_list: 如果是因為update sql table需要刪除redis，要加此參數
    :return:
    """
    update_dict = dict()
    if update_list is None:
        update_list = list()
    for update_data in update_list:
        update_dict[update_data.id] = update_data
    for data in data_list:
        row = schemas_model(**jsonable_encoder(data))
        # 刪除主表
        if key == "id":
            redisDB.hdel(table_name, getattr(row, key))
        # 刪除附表(index table)
        elif not update_list or getattr(update_dict.get(row.id, None), key, None) is not None:
            # sql type 是 json list的情況
            if isinstance(getattr(row, key), list):
                for item in getattr(row, key):
                    value_list = json.loads(redisDB.hget(table_name, item))
                    value_list.remove(row.id)
                    if not value_list:
                        redisDB.hdel(table_name, item)
                    else:
                        redisDB.hset(table_name, item, json.dumps(value_list))
            # sql type 是單一值的情況
            else:
                item = getattr(row, key)
                value_list = json.loads(redisDB.hget(table_name, item))
                value_list.remove(row.id)
                if not value_list:
                    redisDB.hdel(table_name, item)
                else:
                    redisDB.hset(table_name, item, json.dumps(value_list))
    return "Ok"
