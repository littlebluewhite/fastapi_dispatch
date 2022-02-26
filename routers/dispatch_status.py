from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import status_data
from dispatch_function import general_operate
from dispatch_schemas import status_schemas

router = APIRouter(
    prefix="/dispatch_status",
    tags=["status", "Table CRUD API"],
    dependencies=[]
)

status_operate = general_operate.GeneralOperate(status_data)


@router.on_event("startup")
async def status_startup_event():
    status_operate.initial_redis_data()


@router.get("/", response_model=list[status_operate.main_schemas])
async def sql_read_all_dispatch_status(db: Session = Depends(get_db)):
    return status_operate.read_all_data_from_sql(db)


@router.get("/{status_id}", response_model=status_operate.main_schemas)
async def sql_read_dispatch_status(status_id: int, db: Session = Depends(get_db)):
    return status_operate.read_data_from_sql_by_id_set(db, {status_id})[0]


@router.get("/api/multiple/", response_model=list[status_operate.main_schemas])
async def get_multiple_dispatch_status(common: CommonQuery = Depends(),
                                       db: Session = Depends(get_db)):
    if common.pattern == "all":
        return status_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = status_operate.execute_sql_where_command(db, common.where_command)
        return status_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{status_id}", response_model=status_operate.main_schemas)
async def get_dispatch_status_by_id(status_id):
    return status_operate.read_data_from_redis_by_key_set({status_id})[0]


@router.post("/api/", response_model=status_operate.main_schemas)
async def create_dispatch_status(status: status_schemas.DispatchStatusCreate, db: Session = Depends(get_db)):
    with db.begin():
        return status_operate.create_data(db, [status])[0]


@router.post("/api/multiple/", response_model=list[status_operate.main_schemas])
async def create_multiple_dispatch_status(
        status_list: list[status_schemas.DispatchStatusCreate], db: Session = Depends(get_db)):
    with db.begin():
        return status_operate.create_data(db, status_list)


@router.patch("/api/{status_id}", response_model=status_operate.main_schemas)
async def update_dispatch_status(update_data: status_schemas.DispatchStatusUpdate,
                                 status_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [status_operate.add_id_in_update_data(update_data, status_id)]
        return status_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/", response_model=list[status_operate.main_schemas])
async def update_multiple_dispatch_status(
        update_list: list[status_schemas.DispatchStatusMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return status_operate.update_data(db, update_list)


@router.delete("/api/{status_id}")
async def delete_dispatch_status(status_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return status_operate.delete_data(db, {status_id})


@router.delete("/api/multiple/")
async def delete_dispatch_status(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return status_operate.delete_data(db, id_set)
