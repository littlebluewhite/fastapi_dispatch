import base64

from fastapi import APIRouter, UploadFile, Depends, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import sql_operate
from dispatch_data import reply_file_data
from dispatch_data.enum_data import ReplyFileType
from dispatch_function import reply_file_function, general_operate
from dispatch_schemas import reply_file_schemas

router = APIRouter(
    prefix="/dispatch_reply_file",
    tags=["reply_file", "Table CRUD API"],
    dependencies=[]
)

reply_file_operate = general_operate.GeneralOperate(reply_file_data)


@router.on_event("startup")
async def status_startup_event():
    reply_file_operate.initial_redis_data()


@router.post("/multiple/{reply_id}", response_model=list[reply_file_operate.main_schemas])
async def sql_create_reply_files(reply_id: int, files: list[UploadFile],
                                 file_type: ReplyFileType = Form(...),
                                 db: Session = Depends(get_db)):
    with db.begin():
        create_data_list = list()
        for file in files:
            file_path = await reply_file_function.write_reply_file(file, reply_id)
            create_data_list.append(reply_file_schemas.DispatchReplyFileCreate(
                dispatch_reply_id=reply_id, filename=file.filename,
                content_type=file.content_type, file_type=file_type, path=file_path
            ))

        sql_data_list = reply_file_operate.create_data(db, create_data_list)
        return jsonable_encoder(
            sql_data_list, custom_encoder={bytes: lambda v: base64.b64encode(v).decode('utf-8')})


@router.get("/{reply_file_id}")
async def sql_read_reply_file(reply_file_id: int, db: Session = Depends(get_db)):
    file = sql_operate.get_sql_data(db, {reply_file_id}, reply_file_operate.sql_model)[0]
    return StreamingResponse(reply_file_function.file_generator(file.path), media_type=file.content_type)


@router.delete("/multiple/")
async def sql_update_reply_file(reply_file_id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        reply_file_list = reply_file_operate.read_data_from_redis_by_key_set(reply_file_id_set)
        for reply_file in reply_file_list:
            reply_file_function.delete_reply_file(reply_file["path"])
        return reply_file_operate.delete_data(db, reply_file_id_set)
