from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import confirm_data
from dispatch_function import confirm_function
from dispatch_function.reload_function import initial_reload_data_from_sql, reload_redis_task_from_sql
from dispatch_redis import operate
from dispatch_schemas import confirm_schemas

router = APIRouter(
    prefix="/dispatch_confirm",
    tags=["confirm"],
    dependencies=[]
)

redis_tables = confirm_data.redis_tables
sql_model_name = confirm_data.sql_model_name
schemas_model_name = confirm_data.schemas_model_name


@router.on_event("startup")
async def confirm_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=confirm_schemas.DispatchConfirm)
async def sql_create_dispatch_confirm(confirm: confirm_schemas.DispatchConfirmCreate, db: Session = Depends(get_db)):
    return crud.create_sql_data(db, confirm, sql_model_name)


@router.get("/", response_model=list[confirm_schemas.DispatchConfirm])
async def sql_read_all_dispatch_confirm(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{confirm_id}", response_model=confirm_schemas.DispatchConfirm)
async def sql_read_dispatch_confirm(confirm_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, confirm_id, sql_model_name)


@router.patch("/{confirm_id}", response_model=confirm_schemas.DispatchConfirm)
async def sql_update_dispatch_confirm(update_model: confirm_schemas.DispatchConfirmUpdate,
                                      confirm_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_model, confirm_id, sql_model_name)


@router.delete("/{confirm_id}")
async def sql_delete_dispatch_confirm(confirm_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, confirm_id, sql_model_name)


@router.get("/api/", response_model=list[confirm_schemas.DispatchConfirm],
            tags=["Table CURD API"])
async def get_all_dispatch_confirm():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{confirm_id}", response_model=confirm_schemas.DispatchConfirm,
            tags=["Table CURD API"])
async def get_dispatch_confirm_by_id(confirm_id):
    return operate.read_redis_data(redis_tables[0]["name"], confirm_id)


@router.post("/api/", response_model=confirm_schemas.DispatchConfirm,
             tags=["Table CURD API"])
async def create_dispatch_confirm(confirm_create: confirm_schemas.DispatchConfirmCreate, db: Session = Depends(get_db)):
    return confirm_function.create_confirm(confirm_create, db)


@router.patch("/api/{confirm_id}", response_model=confirm_schemas.DispatchConfirm,
              tags=["Table CURD API"])
async def update_dispatch_confirm(update_model: confirm_schemas.DispatchConfirmUpdate,
                                  confirm_id: int, db: Session = Depends(get_db)):
    result = crud.update_sql_data(db, update_model, confirm_id, sql_model_name)
    reload_redis_task_from_sql(db, result.dispatch_task_id)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.delete("/api/{confirm_id}",
               tags=["Table CURD API"])
async def delete_dispatch_confirm(confirm_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, confirm_id, sql_model_name)
    reload_redis_task_from_sql(db, delete_datum.dispatch_task_id)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
