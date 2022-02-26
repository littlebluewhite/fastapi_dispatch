from dispatch_SQL import models
from dispatch_data import task_data
from dispatch_schemas import confirm_schemas

redis_tables = [
    {"name": "dispatch_confirm", "key": "id"},
]
sql_model = models.DispatchConfirm
main_schemas = confirm_schemas.DispatchConfirm
multiple_update_schemas = confirm_schemas.DispatchConfirmMultipleUpdate

reload_related_redis_tables = [
    {"module": task_data, "field": "dispatch_task_id"}
]

confirm_status_to_task_status_dict = {
    "fail": "confirm_fail",
    "success": "confirm_success",
    "other": "confirm_other"
}
