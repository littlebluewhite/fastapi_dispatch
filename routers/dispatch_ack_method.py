from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import ack_method_data
from dispatch_function.reload_function import initial_reload_data_from_sql
from dispatch_redis import operate
from dispatch_schemas import ack_method_schemas

router = APIRouter(
    prefix="/dispatch_ack_method",
    tags=["ack_method"],
    dependencies=[]
)

redis_tables = ack_method_data.redis_tables
sql_model_name = ack_method_data.sql_model_name
schemas_model_name = ack_method_data.schemas_model_name


@router.on_event("startup")
async def ack_method_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=ack_method_schemas.DispatchAckMethod)
async def sql_create_dispatch_ack_method(ack_method: ack_method_schemas.DispatchAckMethodCreate,
                                         db: Session = Depends(get_db)):
    return crud.create_sql_data(db, ack_method, sql_model_name)


@router.get("/", response_model=list[ack_method_schemas.DispatchAckMethod])
async def sql_read_all_dispatch_ack_method(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{ack_method_id}", response_model=ack_method_schemas.DispatchAckMethod)
async def sql_read_dispatch_ack_method(ack_method_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, ack_method_id, sql_model_name)


@router.patch("/{ack_method_id}", response_model=ack_method_schemas.DispatchAckMethod)
async def sql_update_dispatch_ack_method(update_model: ack_method_schemas.DispatchAckMethodUpdate,
                                         ack_method_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_model, ack_method_id, sql_model_name)


@router.delete("/{ack_method_id}")
async def sql_delete_dispatch_ack_method(ack_method_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, ack_method_id, sql_model_name)


@router.get("/api/", response_model=list[ack_method_schemas.DispatchAckMethod],
            tags=["Table CURD API"])
async def get_all_dispatch_ack_method():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{ack_method_id}", response_model=ack_method_schemas.DispatchAckMethod,
            tags=["Table CURD API"])
async def get_dispatch_ack_method_by_id(ack_method_id):
    return operate.read_redis_data(redis_tables[0]["name"], ack_method_id)


@router.post("/api/", response_model=ack_method_schemas.DispatchAckMethod,
             tags=["Table CURD API"])
async def create_dispatch_ack_method(ack_method: ack_method_schemas.DispatchAckMethodCreate,
                                     db: Session = Depends(get_db)):
    result = crud.create_sql_data(db, ack_method, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.patch("/api/{ack_method_id}", response_model=ack_method_schemas.DispatchAckMethod,
              tags=["Table CURD API"])
async def update_dispatch_ack_method(update_model: ack_method_schemas.DispatchAckMethodUpdate,
                                     ack_method_id: int, db: Session = Depends(get_db)):
    result = crud.update_sql_data(db, update_model, ack_method_id, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.delete("/api/{ack_method_id}",
               tags=["Table CURD API"])
async def delete_dispatch_ack_method(ack_method_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, ack_method_id, sql_model_name)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
