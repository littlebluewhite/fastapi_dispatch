import base64

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from dispatch_SQL import crud
from dispatch_data import task_data
from dispatch_redis import operate
from dispatch_schemas import task_schemas


def update_task(update_data: task_schemas.DispatchTaskUpdate,
                task_id: int, db: Session) -> task_schemas.DispatchTask:
    data = crud.update_sql_data(db, update_data, task_id, task_data.sql_model_name)
    for table in task_data.redis_tables:
        operate.write_sql_data_to_redis(table["name"], [data], task_data.schemas_model_name, table["key"])
    return task_schemas.DispatchTask(**jsonable_encoder(data, custom_encoder={
        bytes: lambda v: base64.b64encode(v).decode('utf-8')}))
