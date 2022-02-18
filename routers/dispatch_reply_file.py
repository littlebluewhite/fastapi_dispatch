from fastapi import APIRouter, UploadFile, Depends, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import reply_file_data
from dispatch_data.enum_data import ReplyFileType
from dispatch_function import reply_file_function
from dispatch_schemas import reply_file_schemas

router = APIRouter(
    prefix="/dispatch_reply_file",
    tags=["reply_file"],
    dependencies=[]
)

sql_model_name = reply_file_data.sql_model_name


@router.post("/multiple/{reply_id}", tags=["Table CURD API"])
async def sql_create_reply_files(reply_id: int, files: list[UploadFile],
                                 file_type: ReplyFileType = Form(...),
                                 db: Session = Depends(get_db)):
    return reply_file_function.create_reply_files(db, files, file_type)


@router.post("/{reply_id}", tags=["Table CURD API"], deprecated=True)
async def sql_create_reply_file(reply_id: int, file: UploadFile,
                                file_type: ReplyFileType = Form(...),
                                db: Session = Depends(get_db)):
    create_data = reply_file_schemas.DispatchReplyFileCreate(
        dispatch_reply_id=reply_id, filename=file.filename,
        content_type=file.content_type, file_type=file_type, data=file.file.read()
    )
    sql_datum = crud.create_sql_data(db, create_data, sql_model_name)
    reply_file_function.file_reload_related_redis(db, [sql_datum.dispatch_reply_id])
    return "Ok"


@router.get("/{reply_file_id}", tags=["Table CURD API"])
async def sql_read_reply_file(reply_file_id: int, db: Session = Depends(get_db)):
    file = crud.get_sql_data(db, reply_file_id, sql_model_name)
    return StreamingResponse(reply_file_function.file_generator(file.data), media_type=file.content_type)


@router.delete("/{reply_file_id}", tags=["Table CURD API"])
async def sql_update_reply_file(reply_file_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, reply_file_id, sql_model_name)
    reply_file_function.file_reload_related_redis(db, [delete_datum.dispatch_reply_id])
    return "Ok"
