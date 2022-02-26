import os
import random

import aiofiles as aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from dispatch_data import reply_data, task_data, enum_data
from dispatch_exception import DispatchException
from dispatch_function import reload_function
from dispatch_schemas import reply_file_schemas


def file_generator(path: str):
    with open(path, mode="rb") as f:
        yield from f


def file_reload_related_redis(db: Session, reply_id_set: set):
    # reload reply redis table
    sql_data_list = reload_function.reload_redis_from_sql(
        db, reply_data.sql_model, reply_data.main_schemas,
        reply_data.redis_tables, reply_id_set
    )
    task_id_set = set()
    for datum in sql_data_list:
        task_id_set.add(datum.dispatch_task_id)
    # reload task redis table
    reload_function.reload_redis_from_sql(
        db, task_data.sql_model, task_data.main_schemas,
        task_data.redis_tables, task_id_set
    )


async def write_reply_file(file: UploadFile, reply_id):
    path = f"./static/reply_file/{str(reply_id)}_{int(random.random()*1000)}_{file.filename.replace(' ', '_')}"
    async with aiofiles.open(path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return path


def reply_files_format(reply_id: int, files: list[UploadFile], file_type: enum_data.ReplyFileType):
    return [
        reply_file_schemas.DispatchReplyFileCreate(
            dispatch_reply_id=reply_id, filename=file.filename,
            content_type=file.content_type, file_type=file_type, data=file.file.read()
        ) for file in files
    ]


def delete_reply_file(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        raise DispatchException(status_code=502, detail="server remove file error")
