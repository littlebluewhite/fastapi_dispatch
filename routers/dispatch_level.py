from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import level_data
from dispatch_function.reload_function import initial_reload_data_from_sql
from dispatch_redis import operate
from dispatch_schemas import level_schemas

router = APIRouter(
    prefix="/dispatch_level",
    tags=["level"],
    dependencies=[]
)

redis_tables = level_data.redis_tables
sql_model_name = level_data.sql_model_name
schemas_model_name = level_data.schemas_model_name


@router.on_event("startup")
async def level_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=level_schemas.DispatchLevel)
async def sql_create_dispatch_level(level: level_schemas.DispatchLevelCreate, db: Session = Depends(get_db)):
    return crud.create_sql_data(db, level, sql_model_name)


@router.get("/", response_model=list[level_schemas.DispatchLevel])
async def sql_read_all_dispatch_level(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{level_id}", response_model=level_schemas.DispatchLevel)
async def sql_read_dispatch_level(level_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, level_id, sql_model_name)


@router.patch("/{level_id}", response_model=level_schemas.DispatchLevel)
async def sql_update_dispatch_level(update_model: level_schemas.DispatchLevelUpdate,
                                    level_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_model, level_id, sql_model_name)


@router.delete("/{level_id}")
async def sql_delete_dispatch_level(level_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, level_id, sql_model_name)


@router.get("/api/", response_model=list[level_schemas.DispatchLevel],
            tags=["Table CURD API"])
async def get_all_dispatch_level():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{level_id}", response_model=level_schemas.DispatchLevel,
            tags=["Table CURD API"])
async def get_dispatch_level_by_id(level_id):
    return operate.read_redis_data(redis_tables[0]["name"], level_id)


@router.post("/api/", response_model=level_schemas.DispatchLevel,
             tags=["Table CURD API"])
async def create_dispatch_level(level: level_schemas.DispatchLevelCreate, db: Session = Depends(get_db)):
    result = crud.create_sql_data(db, level, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.patch("/api/{level_id}", response_model=level_schemas.DispatchLevel,
              tags=["Table CURD API"])
async def update_dispatch_level(update_model: level_schemas.DispatchLevelUpdate,
                                level_id: int, db: Session = Depends(get_db)):
    result = crud.update_sql_data(db, update_model, level_id, sql_model_name)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.delete("/api/{level_id}",
               tags=["Table CURD API"])
async def delete_dispatch_level(level_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, level_id, sql_model_name)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
