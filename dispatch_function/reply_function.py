from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dispatch_SQL import crud
from dispatch_data import reply_data
from dispatch_function import reload_function
from dispatch_redis import operate
from dispatch_schemas import reply_schemas


def create_reply(create_data: reply_schemas.DispatchReplyCreate, db: Session)\
        -> reply_schemas.DispatchReply:
    # write in sql table
    create_data = crud.create_sql_data(db, create_data, reply_data.sql_model_name)
    reload_function.reload_redis_task_from_sql(db, create_data.dispatch_task_id)
    # write in redis table
    for table in reply_data.redis_tables:
        operate.write_sql_data_to_redis(table["name"], [create_data], reply_data.schemas_model_name, table["key"])
    return reply_schemas.DispatchReply(**jsonable_encoder(create_data))
