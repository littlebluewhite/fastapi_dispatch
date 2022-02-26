from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import confirm_data
from dispatch_function import general_operate
from dispatch_schemas import confirm_schemas

router = APIRouter(
    prefix="/dispatch_confirm",
    tags=["confirm", "Table CRUD API"],
    dependencies=[]
)

confirm_operate = general_operate.GeneralOperate(confirm_data)


@router.on_event("startup")
async def confirm_startup_event():
    confirm_operate.initial_redis_data()


@router.get("/", response_model=list[confirm_operate.main_schemas])
async def sql_read_all_dispatch_confirm(db: Session = Depends(get_db)):
    return confirm_operate.read_all_data_from_sql(db)


@router.get("/{confirm_id}", response_model=confirm_operate.main_schemas)
async def sql_read_dispatch_confirm(confirm_id: int, db: Session = Depends(get_db)):
    return confirm_operate.read_data_from_sql_by_id_set(db, {confirm_id})[0]


@router.get("/api/multiple/", response_model=list[confirm_operate.main_schemas])
async def get_multiple_dispatch_confirm(common: CommonQuery = Depends(),
                                        db: Session = Depends(get_db)):
    if common.pattern == "all":
        return confirm_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = confirm_operate.execute_sql_where_command(db, common.where_command)
        return confirm_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{confirm_id}", response_model=confirm_operate.main_schemas)
async def get_dispatch_confirm_by_id(confirm_id):
    return confirm_operate.read_data_from_redis_by_key_set({confirm_id})[0]


@router.post("/api/", response_model=confirm_operate.main_schemas)
async def create_dispatch_confirm(confirm: confirm_schemas.DispatchConfirmCreate, db: Session = Depends(get_db)):
    with db.begin():
        return confirm_operate.create_data(db, [confirm])[0]


@router.post("/api/multiple/", response_model=list[confirm_operate.main_schemas])
async def create_multiple_dispatch_confirm(
        confirm_list: list[confirm_schemas.DispatchConfirmCreate], db: Session = Depends(get_db)):
    with db.begin():
        return confirm_operate.create_data(db, confirm_list)


@router.patch("/api/{confirm_id}", response_model=confirm_operate.main_schemas)
async def update_dispatch_confirm(update_data: confirm_schemas.DispatchConfirmUpdate,
                                  confirm_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [confirm_operate.add_id_in_update_data(update_data, confirm_id)]
        return confirm_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/", response_model=list[confirm_operate.main_schemas])
async def update_multiple_dispatch_confirm(
        update_list: list[confirm_schemas.DispatchConfirmMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return confirm_operate.update_data(db, update_list)


@router.delete("/api/{confirm_id}")
async def delete_dispatch_confirm(confirm_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return confirm_operate.delete_data(db, {confirm_id})


@router.delete("/api/multiple/")
async def delete_dispatch_confirm(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return confirm_operate.delete_data(db, id_set)
