from pydantic import BaseModel

from dispatch_data.enum_data import ReplyConfirmStatus


class WorkerReceiveTask(BaseModel):
    task_taker: str
    status_id: int


class DispatcherCreateConfirm(BaseModel):
    provider_name: str
    status: ReplyConfirmStatus
    description: str
