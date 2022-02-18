from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import status_data
from dispatch_function.reload_function import initial_reload_data_from_sql
from dispatch_redis import operate
from dispatch_schemas import status_schemas

router = APIRouter(
    prefix="/dispatch_status",
    tags=["status"],
    dependencies=[]
)

redis_tables = status_data.redis_tables
sql_model_name = status_data.sql_model_name
schemas_model_name = status_data.schemas_model_name


@router.on_event("startup")
async def status_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=status_schemas.DispatchStatus)
async def sql_create_dispatch_status(status: status_schemas.DispatchStatusCreate, db: Session = Depends(get_db)):
    return crud.create_sql_data(db, status, sql_model_name)


@router.get("/", response_model=list[status_schemas.DispatchStatus])
async def sql_read_all_dispatch_status(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{status_id}", response_model=status_schemas.DispatchStatus)
async def sql_read_dispatch_status(status_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, status_id, sql_model_name)


@router.patch("/{status_id}", response_model=status_schemas.DispatchStatus)
async def sql_update_dispatch_status(update_model: status_schemas.DispatchStatusUpdate,
                                     status_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_model, status_id, sql_model_name)


@router.delete("/{status_id}")
async def sql_delete_dispatch_status(status_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, status_id, sql_model_name)


@router.get("/api/", response_model=list[status_schemas.DispatchStatus],
            tags=["Table CURD API"])
async def get_all_dispatch_status():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{status_id}", response_model=status_schemas.DispatchStatus,
            tags=["Table CURD API"])
async def get_dispatch_status_by_id(status_id):
    return operate.read_redis_data(redis_tables[0]["name"], status_id)


@router.post("/api/", response_model=status_schemas.DispatchStatus,
             tags=["Table CURD API"])
async def create_dispatch_status(status: status_schemas.DispatchStatusCreate, db: Session = Depends(get_db)):
    result = crud.create_sql_data(db, status, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.patch("/api/{status_id}", response_model=status_schemas.DispatchStatus,
              tags=["Table CURD API"])
async def update_dispatch_status(update_model: status_schemas.DispatchStatusUpdate,
                                 status_id: int, db: Session = Depends(get_db)):
    result = crud.update_sql_data(db, update_model, status_id, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.delete("/api/{status_id}",
               tags=["Table CURD API"])
async def delete_dispatch_status(status_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, status_id, sql_model_name)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
