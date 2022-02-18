from dispatch_SQL import crud
from dispatch_SQL.crud import get_sql_data
from dispatch_SQL.database import SessionLocal
from dispatch_data import task_data
from dispatch_redis import operate


def initial_reload_data_from_sql(redis_tables: list, sql_model_name, schemas_model_name):
    db = SessionLocal()
    # sql 取資料
    sql_data = crud.get_all_sql_data(db, sql_model_name)
    for table in redis_tables:
        # 清除redis表
        operate.clean_redis_by_name(table["name"])
        # 將sql資料寫入redis表
        operate.write_sql_data_to_redis(table["name"], sql_data, schemas_model_name, table["key"])
    db.close()


def reload_redis_task_from_sql(db, task_id: int):
    result = get_sql_data(db, task_id, task_data.sql_model_name)
    for table in task_data.redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result],
                                        task_data.schemas_model_name, table["key"])


def reload_redis_from_sql(
        db, sql_model_name: str, schemas_model_name: str, redis_tables: list, data_id_list: list):
    sql_data: list = list()
    for data_id in data_id_list:
        datum = get_sql_data(db, data_id, sql_model_name)
        sql_data.append(datum)
    for table in redis_tables:
        operate.write_sql_data_to_redis(
            table["name"], sql_data, schemas_model_name, table["key"])
    return sql_data
