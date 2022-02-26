from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import level_data
from dispatch_function import general_operate
from dispatch_schemas import level_schemas

router = APIRouter(
    prefix="/dispatch_level",
    tags=["level", "Table CRUD API"],
    dependencies=[]
)

level_operate = general_operate.GeneralOperate(level_data)


@router.on_event("startup")
async def level_startup_event():
    level_operate.initial_redis_data()


@router.get("/", response_model=list[level_operate.main_schemas])
async def sql_read_all_dispatch_level(db: Session = Depends(get_db)):
    return level_operate.read_all_data_from_sql(db)


@router.get("/{level_id}", response_model=level_operate.main_schemas)
async def sql_read_dispatch_level(level_id: int, db: Session = Depends(get_db)):
    return level_operate.read_data_from_sql_by_id_set(db, {level_id})[0]


@router.get("/api/multiple/", response_model=list[level_operate.main_schemas])
async def get_multiple_dispatch_level(common: CommonQuery = Depends(),
                                      db: Session = Depends(get_db)):
    if common.pattern == "all":
        return level_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = level_operate.execute_sql_where_command(db, common.where_command)
        return level_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{level_id}", response_model=level_operate.main_schemas)
async def get_dispatch_level_by_id(level_id):
    return level_operate.read_data_from_redis_by_key_set({level_id})[0]


@router.post("/api/", response_model=level_operate.main_schemas)
async def create_dispatch_level(level: level_schemas.DispatchLevelCreate, db: Session = Depends(get_db)):
    with db.begin():
        return level_operate.create_data(db, [level])[0]


@router.post("/api/multiple/", response_model=list[level_operate.main_schemas])
async def create_multiple_dispatch_level(
        level_list: list[level_schemas.DispatchLevelCreate], db: Session = Depends(get_db)):
    with db.begin():
        return level_operate.create_data(db, level_list)


@router.patch("/api/{level_id}", response_model=level_operate.main_schemas)
async def update_dispatch_level(update_data: level_schemas.DispatchLevelUpdate,
                                level_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [level_operate.add_id_in_update_data(update_data, level_id)]
        return level_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/", response_model=list[level_operate.main_schemas])
async def update_multiple_dispatch_level(
        update_list: list[level_schemas.DispatchLevelMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return level_operate.update_data(db, update_list)


@router.delete("/api/{level_id}")
async def delete_dispatch_level(level_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return level_operate.delete_data(db, {level_id})


@router.delete("/api/multiple/")
async def delete_dispatch_level(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return level_operate.delete_data(db, id_set)
