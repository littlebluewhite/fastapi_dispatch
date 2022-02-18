redis_tables = [
    {"name": "dispatch_confirm", "key": "id"},
]
sql_model_name = "DispatchConfirm"
schemas_model_name = "DispatchConfirm"

confirm_status_to_task_status_dict = {
    "fail": "confirm_fail",
    "success": "confirm_success",
    "other": "confirm_other"
}
