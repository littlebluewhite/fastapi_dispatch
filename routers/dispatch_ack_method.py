from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import ack_method_data
from dispatch_function import general_operate
from dispatch_schemas import ack_method_schemas

router = APIRouter(
    prefix="/dispatch_ack_method",
    tags=["ack_method", "Table CRUD API"],
    dependencies=[]
)

ack_method_operate = general_operate.GeneralOperate(ack_method_data)


@router.on_event("startup")
async def ack_method_startup_event():
    ack_method_operate.initial_redis_data()


@router.get("/", response_model=list[ack_method_operate.main_schemas])
async def sql_read_all_dispatch_ack_method(db: Session = Depends(get_db)):
    return ack_method_operate.read_all_data_from_sql(db)


@router.get("/{ack_method_id}", response_model=ack_method_operate.main_schemas)
async def sql_read_dispatch_ack_method(ack_method_id: int, db: Session = Depends(get_db)):
    return ack_method_operate.read_data_from_sql_by_id_set(db, {ack_method_id})[0]


@router.get("/api/nultiple", response_model=list[ack_method_operate.main_schemas])
async def get_multiple_dispatch_ack_method(common: CommonQuery = Depends(),
                                           db: Session = Depends(get_db)):
    if common.pattern == "all":
        return ack_method_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = ack_method_operate.execute_sql_where_command(db, common.where_command)
        return ack_method_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{ack_method_id}", response_model=ack_method_operate.main_schemas)
async def get_dispatch_ack_method_by_id(ack_method_id):
    return ack_method_operate.read_data_from_redis_by_key_set({ack_method_id})[0]


@router.post("/api/", response_model=ack_method_operate.main_schemas)
async def create_dispatch_ack_method(ack_method: ack_method_schemas.DispatchAckMethodCreate,
                                     db: Session = Depends(get_db)):
    with db.begin():
        return ack_method_operate.create_data(db, [ack_method])[0]


@router.post("/api/multiple/", response_model=list[ack_method_operate.main_schemas])
async def create_multiple_dispatch_ack_method(
        ack_method_list: list[ack_method_schemas.DispatchAckMethodCreate], db: Session = Depends(get_db)):
    with db.begin():
        return ack_method_operate.create_data(db, ack_method_list)


@router.patch("/api/{ack_method_id}", response_model=ack_method_operate.main_schemas)
async def update_dispatch_ack_method(update_data: ack_method_schemas.DispatchAckMethodUpdate,
                                     ack_method_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [ack_method_operate.add_id_in_update_data(update_data, ack_method_id)]
        return ack_method_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/", response_model=list[ack_method_operate.main_schemas])
async def update_multiple_dispatch_ack_method(
        update_list: list[ack_method_schemas.DispatchAckMethodMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return ack_method_operate.update_data(db, update_list)


@router.delete("/api/{ack_method_id}")
async def delete_dispatch_ack_method(ack_method_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return ack_method_operate.delete_data(db, {ack_method_id})


@router.delete("/api/multiple/")
async def delete_dispatch_ack_method(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return ack_method_operate.delete_data(db, id_set)
