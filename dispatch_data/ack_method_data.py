from dispatch_SQL import models
from dispatch_schemas import ack_method_schemas

redis_tables = [
    {"name": "dispatch_ack_method", "key": "id"},
]
sql_model = models.DispatchAckMethod
main_schemas = ack_method_schemas.DispatchAckMethod
multiple_update_schemas = ack_method_schemas.DispatchAckMethodMultipleUpdate

reload_related_redis_tables = []
