from typing import Optional

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

import dispatch_schemas.task_schemas as task_schemas
from dependencies.client_api_dependencies import check_active, worker_receive_model, DispatcherConfirm, WorkerReply
from dependencies.db_dependencies import get_db
from dispatch_data import enum_data
from dispatch_function import reply_file_function
from dispatch_schemas import reply_file_schemas
from routers.dispatch_confirm import confirm_operate
from routers.dispatch_reply import reply_operate
from routers.dispatch_reply_file import reply_file_operate
from routers.dispatch_task import task_operate

router = APIRouter(
    prefix="/client_api",
    tags=["Client API"],
    dependencies=[]
)


@router.patch("/worker/receive_task/{task_id}", dependencies=[Depends(check_active)],
              response_model=task_operate.main_schemas)
async def worker_receive_task(task_id: int,
                              update_data: task_schemas.DispatchTaskUpdate = Depends(worker_receive_model),
                              db: Session = Depends(get_db)):
    with db.begin():
        update_list = [task_operate.add_id_in_update_data(update_data, task_id)]
        return task_operate.update_data(db, update_list)[0]


@router.post("/dispatcher/create_confirm/{task_id}", dependencies=[Depends(check_active)],
             response_model=confirm_operate.main_schemas)
async def dispatcher_confirm(params: DispatcherConfirm = Depends()):
    with params.db.begin():
        confirm_create_data = confirm_operate.create_data(params.db, [params.confirm_create_data])[0]
        update_list = [task_operate.add_id_in_update_data(
            params.task_update_data, confirm_create_data.dispatch_task_id)]
        task_operate.update_data(params.db, update_list)
        return confirm_create_data


@router.post("/worker/create_reply/{task_id}", dependencies=[Depends(check_active)])
async def worker_reply(params: WorkerReply = Depends(WorkerReply),
                       video: Optional[list[UploadFile]] = None,
                       photo: Optional[list[UploadFile]] = None):
    with params.db.begin():
        # 創建reply
        reply_create_data = reply_operate.create_sql(params.db, [params.reply_create_date])[0]
        # 創建files
        photo_list = list()
        video_list = list()
        if photo:
            for file in photo:
                file_path = await reply_file_function.write_reply_file(file, reply_create_data.id)
                photo_list.append(reply_file_schemas.DispatchReplyFileCreate(
                    dispatch_reply_id=reply_create_data.id, filename=file.filename,
                    content_type=file.content_type, file_type=enum_data.ReplyFileType("photo"), path=file_path
                ))
        if video:
            for file in video:
                file_path = await reply_file_function.write_reply_file(file, reply_create_data.id)
                video_list.append(reply_file_schemas.DispatchReplyFileCreate(
                    dispatch_reply_id=reply_create_data.id, filename=file.filename,
                    content_type=file.content_type, file_type=enum_data.ReplyFileType("video"), path=file_path
                ))
        if video or photo:
            reply_file_list = reply_file_operate.create_sql(params.db, photo_list+video_list)
            reply_file_operate.update_redis_table(reply_file_list)
        # 更新task
        update_list = [task_operate.add_id_in_update_data(
            params.task_update_data, reply_create_data.dispatch_task_id)]
        task_operate.update_data(params.db, update_list)
        # 很重要! 邏輯點
        params.db.refresh(reply_create_data)
        print("nwe reply file: ", reply_create_data.file)
        # 更新redis
        reply_operate.update_redis_table([reply_create_data])
        # reload 相關 redis
        reply_operate.reload_relative_table(params.db, [reply_create_data])
        return reply_operate.read_data_from_redis_by_key_set({reply_create_data.id})
    # return reply_create_data
