redis_tables = [
    {"name": "dispatch_reply", "key": "id"},
]
sql_model_name = "DispatchReply"
schemas_model_name = "DispatchReply"

reply_status_to_task_status_dict = {
    "fail": "reply_fail",
    "success": "reply_success",
    "other": "reply_other"
}
