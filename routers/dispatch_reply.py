from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db_dependencies import get_db
from dispatch_SQL import crud
from dispatch_data import reply_data
from dispatch_function import reply_function
from dispatch_function.reload_function import initial_reload_data_from_sql, reload_redis_task_from_sql
from dispatch_redis import operate
from dispatch_schemas import reply_schemas

router = APIRouter(
    prefix="/dispatch_reply",
    tags=["reply"],
    dependencies=[]
)

redis_tables = reply_data.redis_tables
sql_model_name = reply_data.sql_model_name
schemas_model_name = reply_data.schemas_model_name


@router.on_event("startup")
async def reply_startup_event():
    initial_reload_data_from_sql(redis_tables, sql_model_name, schemas_model_name)


@router.post("/", response_model=reply_schemas.DispatchReply)
async def sql_create_dispatch_reply(reply: reply_schemas.DispatchReplyCreate, db: Session = Depends(get_db)):
    return crud.create_sql_data(db, reply, sql_model_name)


@router.get("/", response_model=list[reply_schemas.DispatchReply])
async def sql_read_all_dispatch_reply(db: Session = Depends(get_db)):
    return crud.get_all_sql_data(db, sql_model_name)


@router.get("/{reply_id}", response_model=reply_schemas.DispatchReply)
async def sql_read_dispatch_reply(reply_id: int, db: Session = Depends(get_db)):
    return crud.get_sql_data(db, reply_id, sql_model_name)


@router.patch("/{reply_id}", response_model=reply_schemas.DispatchReply)
async def sql_update_dispatch_reply(update_data: reply_schemas.DispatchReplyUpdate,
                                    reply_id: int, db: Session = Depends(get_db)):
    return crud.update_sql_data(db, update_data, reply_id, sql_model_name)


@router.delete("/{reply_id}")
async def sql_delete_dispatch_reply(reply_id: int, db: Session = Depends(get_db)):
    return crud.delete_sql_data(db, reply_id, sql_model_name)


@router.get("/api/", response_model=list[reply_schemas.DispatchReply],
            tags=["Table CURD API"])
async def get_all_dispatch_reply():
    return operate.read_redis_all_data(redis_tables[0]["name"])


@router.get("/api/{reply_id}", response_model=reply_schemas.DispatchReply,
            tags=["Table CURD API"])
async def get_dispatch_reply_by_id(reply_id):
    return operate.read_redis_data(redis_tables[0]["name"], reply_id)


@router.post("/api/", response_model=reply_schemas.DispatchReply,
             tags=["Table CURD API"])
async def create_dispatch_reply(reply_create: reply_schemas.DispatchReplyCreate, db: Session = Depends(get_db)):
    return reply_function.create_reply(reply_create, db)


@router.patch("/api/{reply_id}", response_model=reply_schemas.DispatchReply,
              tags=["Table CURD API"])
async def update_dispatch_reply(update_model: reply_schemas.DispatchReplyUpdate,
                                reply_id: int, db: Session = Depends(get_db)):
    result = crud.update_sql_data(db, update_model, reply_id, sql_model_name)
    reload_redis_task_from_sql(db, result.dispatch_task_id)
    for table in redis_tables:
        operate.write_sql_data_to_redis(table["name"], [result], schemas_model_name, table["key"])
    return result


@router.delete("/api/{reply_id}",
               tags=["Table CURD API"])
async def delete_dispatch_reply(reply_id: int, db: Session = Depends(get_db)):
    delete_datum = crud.delete_sql_data(db, reply_id, sql_model_name)
    reload_redis_task_from_sql(db, delete_datum.dispatch_task_id)
    for table in redis_tables:
        operate.delete_redis_data(table["name"], [delete_datum], schemas_model_name,
                                  table["key"])
    return "Ok"
