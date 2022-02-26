import base64

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import task_data
from dispatch_function import general_operate, task_function, search_function
from dispatch_schemas import task_schemas

router = APIRouter(
    prefix="/dispatch_task",
    tags=["task", "Table CRUD API"],
    dependencies=[]
)

task_operate = general_operate.GeneralOperate(task_data)


@router.on_event("startup")
async def task_startup_event():
    task_operate.initial_redis_data()


@router.get("/", response_model=list[task_operate.main_schemas])
async def sql_read_all_dispatch_tasks(db: Session = Depends(get_db)):
    return task_operate.read_all_data_from_sql(db)


@router.get("/{task_id}", response_model=task_operate.main_schemas)
async def sql_read_dispatch_task(task_id: int, db: Session = Depends(get_db)):
    return task_operate.read_data_from_sql_by_id_set(db, {task_id})[0]


@router.get("/api/multiple/", response_model=list[task_operate.main_schemas])
async def get_multiple_dispatch_task(common: CommonQuery = Depends(), db: Session = Depends(get_db)):
    if common.pattern == "all":
        return task_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = task_operate.execute_sql_where_command(db, common.where_command)
        return task_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{task_id}", response_model=task_operate.main_schemas)
async def get_dispatch_task_by_id(task_id):
    return task_operate.read_data_from_redis_by_key_set({task_id})[0]


@router.post("/api/", response_model=task_operate.main_schemas)
async def create_dispatch_task(task: task_schemas.DispatchTaskCreate, db: Session = Depends(get_db)):
    with db.begin():
        dispatch_event_id = task_function.create_event_id(task.job)
        create_datum = task_schemas.DispatchTaskWrite(**task.dict(), dispatch_event_id=dispatch_event_id)
        return task_operate.create_data(db, [create_datum])[0]


@router.post("/api/multiple/", response_model=list[task_operate.main_schemas])
async def create_multiple_dispatch_task(task_list: list[task_schemas.DispatchTaskCreate],
                                        db: Session = Depends(get_db)):
    with db.begin():
        create_list = list()
        for task in task_list:
            dispatch_event_id = task_function.create_event_id(task.job)
            create_datum = task_schemas.DispatchTaskWrite(**task.dict(), dispatch_event_id=dispatch_event_id)
            create_list.append(create_datum)
        return task_operate.create_data(db, create_list)


@router.patch("/api/{task_id}", response_model=task_operate.main_schemas)
async def update_dispatch_task(update_data: task_schemas.DispatchTaskUpdate,
                               task_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [task_operate.add_id_in_update_data(update_data, task_id)]
        return task_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/}", response_model=list[task_operate.main_schemas])
async def update_multiple_dispatch_task(
        update_list: list[task_schemas.DispatchTaskMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return task_operate.update_data(db, update_list)


@router.delete("/api/{task_id}")
async def delete_dispatch_task(task_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return task_operate.delete_data(db, {task_id})


@router.delete("/api/multiple/")
async def delete_multiple_dispatch_task(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return task_operate.delete_data(db, id_set)
