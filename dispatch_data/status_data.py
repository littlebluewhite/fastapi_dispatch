from dispatch_SQL import models
from dispatch_schemas import status_schemas

redis_tables = [
    {"name": "dispatch_status", "key": "id"},
    {"name": "dispatch_status_by_name", "key": "name"}
]
sql_model = models.DispatchStatus
main_schemas = status_schemas.DispatchStatus
multiple_update_schemas = status_schemas.DispatchStatusMultipleUpdate

reload_related_redis_tables = []
