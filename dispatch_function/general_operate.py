# 1. update the sql table
# 2. update redis tables which the sql table generate
# 3, reload the redis tables which are related to the sql table

from sqlalchemy.orm import Session
from dispatch_SQL import sql_operate
from dispatch_function import reload_function, search_function
from dispatch_redis import redis_operate


class GeneralOperate:
    def __init__(self, module):
        self.module = module
        self.redis_tables = module.redis_tables
        self.sql_model = module.sql_model
        self.sql_table_name = module.sql_model.__tablename__
        self.main_schemas = module.main_schemas
        self.multiple_update_schemas = module.multiple_update_schemas
        self.reload_related_redis_tables = module.reload_related_redis_tables

    # reload redis table from sql for INITIAL
    def initial_redis_data(self):
        reload_function.initial_reload_data_from_sql(self.redis_tables, self.sql_model, self.main_schemas)

    def read_all_data_from_sql(self, db) -> list:
        return sql_operate.get_all_sql_data(db, self.sql_model)

    def read_data_from_sql_by_id_set(self, db, id_set: set) -> list:
        return sql_operate.get_sql_data(db, id_set, self.sql_model)

    def read_all_data_from_redis(self, table_index: int = 0) -> list:
        return redis_operate.read_redis_all_data(self.redis_tables[table_index]["name"])

    def read_data_from_redis_by_key_set(self, key_set: set, table_index: int = 0) -> list[dict]:
        return redis_operate.read_redis_data(self.redis_tables[table_index]["name"], key_set)

    def create_data(self, db: Session, data_list: list) -> list:
        sql_data_list = sql_operate.create_multiple_sql_data(db, data_list, self.sql_model)
        for table in self.redis_tables:
            redis_operate.write_sql_data_to_redis(
                table["name"], sql_data_list, self.main_schemas, table["key"]
            )
        reload_function.reload_redis_table(db, self.reload_related_redis_tables, sql_data_list)
        return sql_data_list

    def update_data(self, db: Session, update_list: list) -> list:
        # 取得更新前的reference id
        original_data_list = self.read_data_from_redis_by_key_set({i.id for i in update_list})
        original_ref_id_dict = self.get_original_ref_id([self.main_schemas(**i) for i in original_data_list])
        # 刪除有關聯的redis資料
        for table in self.redis_tables[1:]:
            redis_operate.delete_redis_data(
                table["name"], original_data_list, self.main_schemas, table["key"], update_list
            )
        # 更新SQL
        sql_data_list = sql_operate.update_multiple_sql_data(db, update_list, self.sql_model)
        for table in self.redis_tables:
            redis_operate.write_sql_data_to_redis(
                table["name"], sql_data_list, self.main_schemas, table["key"]
            )
        reload_function.reload_redis_table(
            db, self.reload_related_redis_tables, sql_data_list, original_ref_id_dict)
        return sql_data_list

    def delete_data(self, db: Session, id_set: set[int]) -> str:
        sql_data_list = sql_operate.delete_multiple_sql_data(db, id_set, self.sql_model)
        for table in self.redis_tables:
            redis_operate.delete_redis_data(
                table["name"], sql_data_list, self.main_schemas, table["key"]
            )
        reload_function.reload_redis_table(db, self.reload_related_redis_tables, sql_data_list)
        return "Ok"

    def add_id_in_update_data(self, update_data, data_id):
        return self.multiple_update_schemas(**update_data.dict(), id=data_id)

    def create_sql(self, db, data_list: list) -> list:
        return sql_operate.create_multiple_sql_data(db, data_list, self.sql_model)

    def update_sql(self, db, update_list: list) -> list:
        return sql_operate.update_multiple_sql_data(db, update_list, self.sql_model)

    def delete_sql(self, db, id_set: set) -> list:
        return sql_operate.delete_multiple_sql_data(db, id_set, self.sql_model)

    def update_redis_table(self, sql_data_list: list):
        for table in self.redis_tables:
            redis_operate.write_sql_data_to_redis(
                table["name"], sql_data_list, self.main_schemas, table["key"]
            )

    def reload_relative_table(self, db: Session, sql_data_list: list, original_ref_id_dict=None):
        if original_ref_id_dict is None:
            original_ref_id_dict = dict()
        reload_function.reload_redis_table(db, self.reload_related_redis_tables, sql_data_list, original_ref_id_dict)

    # 取得原本未被更改的reference的id
    def get_original_ref_id(self, update_list) -> dict:
        result = dict()
        if self.reload_related_redis_tables:
            for table in self.reload_related_redis_tables:
                id_set = {getattr(i, table["field"]) for i in update_list}
                result[table["field"]] = id_set
        # print("result: ", result)
        return result

    def combine_sql_command(self, where_command):
        return search_function.combine_sql_command(self.sql_table_name, where_command)

    def execute_sql_where_command(self, db: Session, where_command) -> set:
        stmt = self.combine_sql_command(where_command)
        id_set = {i[0] for i in db.execute(stmt)}
        return id_set
