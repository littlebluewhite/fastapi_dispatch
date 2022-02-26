from dispatch_SQL import models
from dispatch_data import task_data
from dispatch_schemas import reply_schemas

redis_tables = [
    {"name": "dispatch_reply", "key": "id"},
]
sql_model = models.DispatchReply
main_schemas = reply_schemas.DispatchReply
multiple_update_schemas = reply_schemas.DispatchReplyMultipleUpdate

reload_related_redis_tables = [
    {"module": task_data, "field": "dispatch_task_id"}
]

reply_status_to_task_status_dict = {
    "fail": "reply_fail",
    "success": "reply_success",
    "other": "reply_other"
}
