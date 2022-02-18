from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dispatch_schemas.task_schemas as task_schemas
from dependencies.client_api_dependencies import check_active, worker_receive_model, DispatcherConfirm, WorkerReply
from dependencies.db_dependencies import get_db
from dispatch_data import enum_data
from dispatch_function import confirm_function, task_function, reply_function, reply_file_function
from dispatch_redis import operate

router = APIRouter(
    prefix="/client_api",
    tags=["Client API"],
    dependencies=[]
)


@router.patch("/worker/receive_task/{task_id}", dependencies=[Depends(check_active)],
              response_model=task_schemas.DispatchTask)
def worker_receive_task(task_id: int,
                        update_data: task_schemas.DispatchTaskUpdate = Depends(worker_receive_model),
                        db: Session = Depends(get_db)):
    return task_function.update_task(update_data, task_id, db)


@router.post("/dispatcher/create_confirm/{task_id}", dependencies=[Depends(check_active)])
def dispatcher_confirm(params: DispatcherConfirm = Depends()):
    confirm_create_data = confirm_function.create_confirm(params.confirm_create_data, params.db)
    params.db.close()
    task_function.update_task(params.task_update_data,
                              confirm_create_data.dispatch_task_id,
                              params.db)
    return confirm_create_data


@router.post("/worker/create_reply/{task_id}", dependencies=[Depends(check_active)])
def worker_reply(params: WorkerReply = Depends()):
    reply_create_data = reply_function.create_reply(params.reply_create_date, params.db)
    params.db.close()
    if params.photo:
        reply_file_function.create_reply_files(
            params.db, reply_create_data.id, params.photo,
            enum_data.ReplyFileType("photo"))
    params.db.close()
    if params.video:
        reply_file_function.create_reply_files(
            params.db, reply_create_data.id, params.video,
            enum_data.ReplyFileType("video"))
    params.db.close()
    task_function.update_task(params.task_update_data,
                              reply_create_data.dispatch_task_id,
                              params.db)
    return operate.read_redis_data("dispatch_reply", str(reply_create_data.id))
