from dispatch_SQL import models
from dispatch_schemas import task_schemas

redis_tables = [
    {"name": "dispatch_task", "key": "id"},
    {"name": "dispatch_task_bind_event_id", "key": "bind_event_id"},
    {"name": "dispatch_task_order_taker", "key": "order_taker"}
]
sql_model = models.DispatchTask
main_schemas = task_schemas.DispatchTask
multiple_update_schemas = task_schemas.DispatchTaskMultipleUpdate

reload_related_redis_tables = []
