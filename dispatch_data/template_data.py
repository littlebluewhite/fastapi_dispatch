from dispatch_SQL import models
from dispatch_schemas import template_schemas

redis_tables = [
    {"name": "dispatch_template", "key": "id"},
]
sql_model = models.DispatchTemplate
main_schemas = template_schemas.DispatchTemplate
multiple_update_schemas = template_schemas.DispatchTemplateMultipleUpdate

reload_related_redis_tables = []
