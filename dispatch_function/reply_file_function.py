from fastapi import UploadFile
from sqlalchemy.orm import Session

from dispatch_SQL import crud
from dispatch_data import reply_data, task_data, enum_data, reply_file_data
from dispatch_function import reload_function
from dispatch_schemas import reply_file_schemas


async def file_generator(bytes_data: bytes, chunk: int = 64):
    while bytes_data:
        yield bytes_data[:chunk]
        bytes_data = bytes_data[chunk:]


def file_reload_related_redis(db: Session, reply_id_list: list):
    data_list = reload_function.reload_redis_from_sql(
        db, reply_data.sql_model_name, reply_data.schemas_model_name,
        reply_data.redis_tables, reply_id_list
    )
    task_id_list = list()
    for datum in data_list:
        task_id_list.append(datum.dispatch_task_id)
    reload_function.reload_redis_from_sql(
        db, task_data.sql_model_name, task_data.schemas_model_name,
        task_data.redis_tables, task_id_list
    )


def create_reply_files(db: Session, reply_id: int, files: list[UploadFile],
                       file_type: enum_data.ReplyFileType):
    for file in files:
        create_data = reply_file_schemas.DispatchReplyFileCreate(
            dispatch_reply_id=reply_id, filename=file.filename,
            content_type=file.content_type, file_type=file_type, data=file.file.read()
        )
        crud.create_sql_data(db, create_data, reply_file_data.sql_model_name)
        db.close()
    file_reload_related_redis(db, [reply_id])
    return "Ok"
