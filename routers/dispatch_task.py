from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import task_data
from dispatch_function import task_function
from dispatch_function.reload_function import initial_reload_data_from_sql
from dispatch_redis import operate
from dispatch_schemas import task_schemas

router = APIRouter(
    prefix="/dispatch_task",
    tags=["task"],
    dependencies=[]
)

redis_tables = task_data.redis_tables
sql_model_name = task_data.sql_model_name
schemas_model_name = task_data.schemas_model_name


@router.on_event("startup")
async def task_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=task_schemas.DispatchTask)
async def sql_create_dispatch_task(task: task_schemas.DispatchTaskCreate, db: Session = Depends(get_db)):
    return crud.create_dispatch_task(db=db, task=task)


@router.get("/", response_model=list[task_schemas.DispatchTask])
async def sql_read_all_dispatch_tasks(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{task_id}", response_model=task_schemas.DispatchTask)
async def sql_read_dispatch_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, task_id, sql_model_name)


@router.patch("/{task_id}", response_model=task_schemas.DispatchTask)
async def sql_update_dispatch_task(update_model: task_schemas.DispatchTaskUpdate,
                                   task_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_model, task_id, sql_model_name)


@router.delete("/{task_id}")
async def sql_delete_dispatch_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, task_id, sql_model_name)


@router.get("/api/", response_model=list[task_schemas.DispatchTask],
            tags=["Table CURD API"])
async def get_all_dispatch_task():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{task_id}", response_model=task_schemas.DispatchTask,
            tags=["Table CURD API"])
async def get_dispatch_task_by_id(task_id):
    return operate.read_redis_data(redis_tables[0]["name"], task_id)


@router.post("/api/", response_model=task_schemas.DispatchTask,
             tags=["Table CURD API"])
async def create_dispatch_task(task: task_schemas.DispatchTaskCreate, db: Session = Depends(get_db)):
    result = crud.create_dispatch_task(db, task)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.patch("/api/{task_id}", response_model=task_schemas.DispatchTask,
              tags=["Table CURD API"])
async def update_dispatch_task(update_data: task_schemas.DispatchTaskUpdate,
                               task_id: int, db: Session = Depends(get_db)):
    return task_function.update_task(update_data, task_id, db)


@router.delete("/api/{task_id}",
               tags=["Table CURD API"])
async def delete_dispatch_task(task_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, task_id, sql_model_name)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
