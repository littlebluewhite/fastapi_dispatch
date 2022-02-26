from dispatch_SQL import models
from dispatch_data import reply_data
from dispatch_schemas import reply_file_schemas

redis_tables = [
    {"name": "dispatch_reply_file", "key": "id"}
]
sql_model = models.DispatchReplyFile
main_schemas = reply_file_schemas.DispatchReplyFile
multiple_update_schemas = reply_file_schemas.DispatchReplyFileMultipleUpdate

reload_related_redis_tables = [
    {"module": reply_data, "field": "dispatch_reply_id"}
]
