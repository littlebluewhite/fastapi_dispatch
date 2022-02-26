from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.common_search_dependencies import CommonQuery
from dependencies.db_dependencies import get_db
from dispatch_data import template_data
from dispatch_function import general_operate
from dispatch_schemas import template_schemas

router = APIRouter(
    prefix="/dispatch_template",
    tags=["template", "Table CRUD API"],
    dependencies=[]
)

template_operate = general_operate.GeneralOperate(template_data)


@router.on_event("startup")
async def template_startup_event():
    template_operate.initial_redis_data()


@router.get("/", response_model=list[template_operate.main_schemas])
async def sql_read_all_dispatch_template(db: Session = Depends(get_db)):
    return template_operate.read_all_data_from_sql(db)


@router.get("/{template_id}", response_model=template_operate.main_schemas)
async def sql_read_dispatch_template(template_id: int, db: Session = Depends(get_db)):
    return template_operate.read_data_from_sql_by_id_set(db, {template_id})[0]


@router.get("/api/multiple/", response_model=list[template_operate.main_schemas])
async def get_multiple_dispatch_template(common: CommonQuery = Depends(),
                                         db: Session = Depends(get_db)):
    if common.pattern == "all":
        return template_operate.read_all_data_from_redis()[common.skip:][:common.limit]
    else:
        id_set = template_operate.execute_sql_where_command(db, common.where_command)
        return template_operate.read_data_from_redis_by_key_set(id_set)[common.skip:][:common.limit]


@router.get("/api/{template_id}", response_model=template_operate.main_schemas)
async def get_dispatch_template_by_id(template_id):
    return template_operate.read_data_from_redis_by_key_set({template_id})[0]


@router.post("/api/", response_model=template_operate.main_schemas)
async def create_dispatch_template(template: template_schemas.DispatchTemplateCreate,
                                   db: Session = Depends(get_db)):
    with db.begin():
        return template_operate.create_data(db, [template])[0]


@router.post("/api/multiple/", response_model=list[template_operate.main_schemas])
async def create_multiple_dispatch_template(
        template_list: list[template_schemas.DispatchTemplateCreate], db: Session = Depends(get_db)):
    with db.begin():
        return template_operate.create_data(db, template_list)


@router.patch("/api/{template_id}", response_model=template_operate.main_schemas)
async def update_dispatch_template(update_data: template_schemas.DispatchTemplateUpdate,
                                   template_id: int, db: Session = Depends(get_db)):
    with db.begin():
        update_list = [template_operate.add_id_in_update_data(update_data, template_id)]
        return template_operate.update_data(db, update_list)[0]


@router.patch("/api/multiple/", response_model=list[template_operate.main_schemas])
async def update_multiple_dispatch_template(
        update_list: list[template_schemas.DispatchTemplateMultipleUpdate], db: Session = Depends(get_db)):
    with db.begin():
        return template_operate.update_data(db, update_list)


@router.delete("/api/{template_id}")
async def delete_dispatch_template(template_id: int, db: Session = Depends(get_db)):
    with db.begin():
        return template_operate.delete_data(db, {template_id})


@router.delete("/api/multiple/")
async def delete_dispatch_template(id_set: set[int], db: Session = Depends(get_db)):
    with db.begin():
        return template_operate.delete_data(db, id_set)
