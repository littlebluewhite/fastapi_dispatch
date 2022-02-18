from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import template_data
from dispatch_function.reload_function import initial_reload_data_from_sql
from dispatch_redis import operate
from dispatch_schemas import template_schemas

router = APIRouter(
    prefix="/dispatch_template",
    tags=["template"],
    dependencies=[]
)

redis_tables = template_data.redis_tables
sql_model_name = template_data.sql_model_name
schemas_model_name = template_data.schemas_model_name


@router.on_event("startup")
async def template_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=template_schemas.DispatchTemplate)
async def sql_create_dispatch_template(template: template_schemas.DispatchTemplateCreate,
                                       db: Session = Depends(get_db)):
    return crud.create_sql_data(db, template, sql_model_name)


@router.get("/", response_model=list[template_schemas.DispatchTemplate])
async def sql_read_all_dispatch_template(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{template_id}", response_model=template_schemas.DispatchTemplate)
async def sql_read_dispatch_template(template_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, template_id, sql_model_name)


@router.patch("/{template_id}", response_model=template_schemas.DispatchTemplate)
async def sql_update_dispatch_template(update_model: template_schemas.DispatchTemplateUpdate,
                                       template_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_model, template_id, sql_model_name)


@router.delete("/{template_id}")
async def sql_delete_dispatch_template(template_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, template_id, sql_model_name)


@router.get("/api/", response_model=list[template_schemas.DispatchTemplate],
            tags=["Table CURD API"])
async def get_all_dispatch_template():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{template_id}", response_model=template_schemas.DispatchTemplate,
            tags=["Table CURD API"])
async def get_dispatch_template_by_id(template_id):
    return operate.read_redis_data(redis_tables[0]["name"], template_id)


@router.post("/api/", response_model=template_schemas.DispatchTemplate,
             tags=["Table CURD API"])
async def create_dispatch_template(template: template_schemas.DispatchTemplateCreate, db: Session = Depends(get_db)):
    result = crud.create_sql_data(db, template, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.patch("/api/{template_id}", response_model=template_schemas.DispatchTemplate,
              tags=["Table CURD API"])
async def update_dispatch_template(update_model: template_schemas.DispatchTemplateUpdate,
                                   template_id: int, db: Session = Depends(get_db)):
    result = crud.update_sql_data(db, update_model, template_id, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.delete("/api/{template_id}",
               tags=["Table CURD API"])
async def delete_dispatch_template(template_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, template_id, sql_model_name)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
