import datetime
from typing import Optional

from fastapi import Path, Depends, Body, UploadFile, Form
from sqlalchemy.orm import Session

from dependencies.db_dependencies import get_db
from dispatch_data import confirm_data, enum_data, reply_data
from dispatch_exception import DispatchException
from dispatch_redis import redis_operate
from dispatch_schemas import client_api_schemas, confirm_schemas, task_schemas, ack_method_schemas, reply_schemas


async def get_task_by_id(task_id: str = Path(...)):
    table_name = "dispatch_task"
    return task_schemas.DispatchTask(**redis_operate.read_redis_data(table_name, {task_id})[0])


async def check_active(task_table: task_schemas.DispatchTask = Depends(get_task_by_id)):
    is_active = task_table.isActive
    if not is_active:
        raise DispatchException(status_code=403,
                                detail="Dispatch task inactive")


async def check_people_limit(task_table: task_schemas.DispatchTask = Depends(get_task_by_id)):
    people_limit = task_table.people_limit
    order_taker = task_table.order_taker
    if people_limit <= len(order_taker):
        raise DispatchException(status_code=403,
                                detail="The number of people has reached the limit")
    return order_taker


async def worker_receive_status_id(task_table: task_schemas.DispatchTask = Depends(get_task_by_id)):
    status_id = task_table.status_id
    pending_status_id = redis_operate.read_redis_data("dispatch_status_by_name", {"pending"})[0][0]
    if status_id == pending_status_id:
        # 若status是pending更改為in_progree
        return redis_operate.read_redis_data("dispatch_status_by_name", {"in_progress"})[0][0]
    # 其他status則不改status_id
    return None


async def worker_receive_model(status_id: int = Depends(worker_receive_status_id),
                               order_taker: list = Depends(check_people_limit),
                               task_taker: str = Body(..., embed=True)):
    if task_taker in order_taker:
        raise DispatchException(status_code=406, detail=f"{task_taker} is already in order taker list")
    order_taker.append(task_taker)
    return task_schemas.DispatchTaskUpdate(order_taker=order_taker,
                                           status_id=status_id)


async def confirm_change_task(client_data: client_api_schemas.DispatcherCreateConfirm) \
        -> task_schemas.DispatchTaskUpdate:
    confirm_status = client_data.status.value
    task_status_name = confirm_data.confirm_status_to_task_status_dict[confirm_status]
    status_id = redis_operate.read_redis_data("dispatch_status_by_name", {task_status_name})[0][0]
    if confirm_status == "other":
        task_active = None
        task_end_time = None
    else:
        # 關閉task
        task_active = False
        task_end_time = datetime.datetime.now()
    return task_schemas.DispatchTaskUpdate(status_id=status_id,
                                           isActive=task_active,
                                           end_time=task_end_time)


class DispatcherConfirm:
    def __init__(self, task_id: int, client_data: client_api_schemas.DispatcherCreateConfirm,
                 task_update_data: task_schemas.DispatchTaskUpdate = Depends(confirm_change_task),
                 db: Session = Depends(get_db)):
        confirm_create_data = confirm_schemas.DispatchConfirmCreate(
            dispatch_task_id=task_id,
            **client_data.dict()
        )
        self.confirm_create_data = confirm_create_data
        self.db = db
        self.task_update_data = task_update_data


async def get_ack_method_by_task(task_table: task_schemas.DispatchTask = Depends(get_task_by_id)):
    ack_method_id = task_table.ack_method_id
    table_name = "dispatch_ack_method"
    result = ack_method_schemas.DispatchAckMethod(**redis_operate.read_redis_data(table_name, {str(ack_method_id)})[0])
    if not result:
        raise DispatchException(status_code=404, detail="not get ack method")
    return result


async def check_ack_method(
        video: Optional[list[UploadFile]] = None,
        photo: Optional[list[UploadFile]] = None,
        description: str = Form(None),
        ack_method: ack_method_schemas.DispatchAckMethod = Depends(get_ack_method_by_task),
        status: enum_data.ReplyConfirmStatus = Form(...)):
    reply_status_value = status.value
    is_raise_except = False
    except_msg = "not meet the ack needs( "
    if ack_method.need_text:
        if not description:
            is_raise_except = True
            except_msg += "description "
    if ack_method.need_photo:
        if not photo:
            is_raise_except = True
            except_msg += "photo "
    if ack_method.need_video:
        if not video:
            is_raise_except = True
            except_msg += "video "
    if is_raise_except and reply_status_value == "success":
        raise DispatchException(status_code=402, detail=except_msg + ")")
    return {
        "description": description,
    }


async def check_worker_name(worker_name: str = Form(...),
                            task_table: task_schemas.DispatchTask = Depends(get_task_by_id)):
    order_taker = task_table.order_taker
    if worker_name not in order_taker:
        raise DispatchException(status_code=403, detail="worker did not receive the task")
    return worker_name


async def reply_change_task(status: enum_data.ReplyConfirmStatus = Form(...)):
    reply_status = status.value
    task_status_name = reply_data.reply_status_to_task_status_dict[reply_status]
    status_id = redis_operate.read_redis_data("dispatch_status_by_name", {task_status_name})[0][0]
    return task_schemas.DispatchTaskUpdate(status_id=status_id)


class WorkerReply:
    def __init__(self, task_id: int, content_data: dict = Depends(check_ack_method),
                 worker_name: str = Depends(check_worker_name),
                 task_update_data: task_schemas.DispatchTaskUpdate = Depends(reply_change_task),
                 status: enum_data.ReplyConfirmStatus = Form(...),
                 db: Session = Depends(get_db)
                 ):
        self.reply_create_date = reply_schemas.DispatchReplyCreate(
            dispatch_task_id=task_id,
            worker_name=worker_name,
            status=status.value,
            description=content_data["description"]
        )
        self.task_update_data = task_update_data
        self.db = db
