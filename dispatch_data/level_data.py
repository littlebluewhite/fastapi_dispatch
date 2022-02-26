from dispatch_SQL import models
from dispatch_schemas import level_schemas

redis_tables = [
    {"name": "dispatch_level", "key": "id"},
]
sql_model = models.DispatchLevel
main_schemas = level_schemas.DispatchLevel
multiple_update_schemas = level_schemas.DispatchLevelMultipleUpdate

reload_related_redis_tables = []
