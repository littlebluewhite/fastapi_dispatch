from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import reply_data
from dispatch_function import general_operate
from dispatch_schemas import reply_schemas

router = APIRouter(
    prefix="/dispatch_reply",
    tags=["reply", "Table CRUD API"],
    dependencies=[]
)

reply_operate = general_operate.GeneralOperate(reply_data)


@router.on_event("startup")
async def reply_startup_event():
    reply_operate.initial_redis_data()


@router.get("/", response_model=list[reply_operate.main_schemas])
async def sql_read_all_dispatch_reply(db: Session = Depends(get_db)):
    return reply_operate.read_all_data_from_sql(db)


@router.get("/{reply_id}", response_model=reply_operate.main_schemas)
async def sql_read_dispatch_reply(reply_id: int, db: Session = Depends(get_db)):
    return reply_operate.read_data_from_sql_by_id_set(db, {reply_id})[0]


@router.get("/api/multiple/", response_model=list[reply_operate.main_schemas])
async def get_multiple_dispatch_reply(common: CommonQuery = Depends(),
                                      db: Session = Depends(get_db)):
    if common.pattern == "all":
        return reply_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = reply_operate.execute_sql_where_command(db, common.where_command)
        return reply_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{reply_id}", response_model=reply_operate.main_schemas)
async def get_dispatch_reply_by_id(reply_id):
    return reply_operate.read_data_from_redis_by_key_set({reply_id})[0]


@router.post("/api/", response_model=reply_operate.main_schemas)
async def create_dispatch_reply(reply: reply_schemas.DispatchReplyCreate, db: Session = Depends(get_db)):
    with db.begin():
        return reply_operate.create_data(db, [reply])[0]


@router.post("/api/multiple/", response_model=list[reply_operate.main_schemas])
async def create_multiple_dispatch_reply(
        reply_list: list[reply_schemas.DispatchReplyCreate], db: Session = Depends(get_db)):
    with db.begin():
        return reply_operate.create_data(db, reply_list)


@router.patch("/api/{reply_id}", response_model=reply_operate.main_schemas)
async def update_dispatch_reply(update_data: reply_schemas.DispatchReplyUpdate,
                                reply_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [reply_operate.add_id_in_update_data(update_data, reply_id)]
        return reply_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/", response_model=list[reply_operate.main_schemas])
async def update_multiple_dispatch_reply(
        update_list: list[reply_schemas.DispatchReplyMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return reply_operate.update_data(db, update_list)


@router.delete("/api/{reply_id}")
async def delete_dispatch_reply(reply_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return reply_operate.delete_data(db, {reply_id})


@router.delete("/api/multiple/")
async def delete_dispatch_reply(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return reply_operate.delete_data(db, id_set)
