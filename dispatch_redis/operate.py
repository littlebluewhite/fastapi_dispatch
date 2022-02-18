import base64
import json

from fastapi.encoders import jsonable_encoder
from dispatch_data.schemas_model_data import schemas_model_dict
from dispatch_exception import DispatchException
from dispatch_redis.redis import redisDB


def clean_redis_by_name(table_name):
    if redisDB.exists(table_name):
        if redisDB.delete(table_name) == 1:
            print(f"clean redis table: {table_name}")


def write_sql_data_to_redis(table_name: str, sql_data: list, schemas_model_name: str,
                            key: str = "id"):
    schemas = schemas_model_dict[schemas_model_name]
    result = list()
    for datum in sql_data:
        row = schemas(**jsonable_encoder(datum, custom_encoder={
            bytes: lambda v: base64.b64encode(v).decode('utf-8')}))
        if key == "id":
            value = row.json()
        else:
            value = row.id
        redisDB.hset(table_name, getattr(row, key), value)
        result.append(row)
    return result


def read_redis_all_data(table_name: str):
    result = []
    for datum in redisDB.hvals(table_name):
        result.append(json.loads(datum))
    return result


def read_redis_data(table_name: str, data_key: str):
    result = redisDB.hget(table_name, data_key)
    if not result:
        raise DispatchException(status_code=404, detail=f"id:{data_key} is not exist")
    return json.loads(result)


def delete_redis_data(table_name: str, delete_data: list, schemas_model_name: str,
                      key: str = "id"):
    schemas = schemas_model_dict[schemas_model_name]
    for datum in delete_data:
        row = schemas(**jsonable_encoder(datum))
        redisDB.hdel(table_name, getattr(row, key))
    return "Ok"
