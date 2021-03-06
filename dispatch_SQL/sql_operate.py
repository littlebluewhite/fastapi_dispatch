import base64

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from dispatch_SQL import models
from dispatch_SQL.database import SessionLocal
from dispatch_exception import DispatchException


def create_multiple_sql_data(db: Session, create_list: list, sql_model) -> list:
    try:
        add_list = list()
        for datum in create_list:
            datum = sql_model(**datum.dict())
            add_list.append(datum)
            db.add_all(add_list)
        db.flush()
        result = list()
        for datum in add_list:
            db.refresh(datum)
            result.append(datum)
        return result
    except IntegrityError as e:
        code, msg = e.orig.args
        if code == 1452:
            raise DispatchException(status_code=403, detail=msg)
        elif code == 1062:
            raise DispatchException(status_code=403, detail=msg)


def get_sql_data(db: Session, id_set: set, sql_model) -> list:
    data_list = db.query(sql_model).filter(sql_model.id.in_(id_set)).all()
    if not data_list:
        raise DispatchException(status_code=404, detail=f"one or more id are not in {id_set}")
    return data_list


def get_all_sql_data(db: Session, sql_model):
    skip: int = 0
    limit: int = 100
    result = list()
    while db.query(sql_model).offset(skip).limit(limit).all():
        result += db.query(sql_model).offset(skip).limit(limit).all()
        skip = limit
        limit += 100
    return [jsonable_encoder(i) for i in result]


# def update_sql_data_by_id(db: Session, update_data, data_id: int, sql_model):
#     try:
#         datum = db.query(sql_model).filter(sql_model.id == data_id).first()
#         if not datum:
#             raise DispatchException(status_code=404, detail=f"id:{data_id} not found")
#         for item in update_data:
#             if item[1] is not None:
#                 setattr(datum, item[0], item[1])
#         db.flush()
#         db.refresh(datum)
#         return datum
#     except IntegrityError as e:
#         code, msg = e.orig.args
#         if code == 1452:
#             raise DispatchException(status_code=403, detail=msg)
#         elif code == 1406:
#             raise DispatchException(status_code=403, detail=msg)


def update_multiple_sql_data(db: Session, update_list: list, sql_model):
    try:
        sql_data_list = list()
        for row in update_list:
            datum = db.query(sql_model).filter(sql_model.id == row.id).first()
            if not datum:
                raise DispatchException(status_code=404, detail=f"id:{row.id} not found")
            for item in row:
                if item[1] is not None and item[0] != "id":
                    setattr(datum, item[0], item[1])
            db.flush()
            db.refresh(datum)
            sql_data_list.append(datum)
        return sql_data_list
    except IntegrityError as e:
        code, msg = e.orig.args
        if code == 1452:
            raise DispatchException(status_code=403, detail=msg)
        elif code == 1406:
            raise DispatchException(status_code=403, detail=msg)


def delete_multiple_sql_data(db: Session, id_set: set, sql_model):
    try:
        delete_data_list = db.query(sql_model).filter(sql_model.id.in_(id_set)).all()
        if len(id_set) != len(delete_data_list):
            raise DispatchException(status_code=404, detail=f"id: one or many of {str(id_set)} is not exist")
        stmt = delete(sql_model).where(sql_model.id.in_(id_set))
        db.execute(stmt)
        db.flush()
        return delete_data_list
    except UnmappedInstanceError:
        raise DispatchException(status_code=404, detail=f"id: one or more of {str(id_set)} is not exist")


if __name__ == "__main__":
    db2 = SessionLocal()
    print(jsonable_encoder(db2.query(models.DispatchTask).join(
        models.DispatchStatus, models.DispatchTask.status_id == models.DispatchStatus.id).all(),
                           custom_encoder={bytes: lambda v: base64.b64encode(v).decode('utf-8')}))
    # ex = db2.query(models.DispatchTask).filter(models.DispatchTask.id == 2).first()\
    # print(type(jsonable_encoder(ex)))
    # a = task_schemas.DispatchTask(**jsonable_encoder(ex), confirm=ex.confirm)
    # print(a.json())
    # b = status_schemas.DispatchStatus(**jsonable_encoder(ex.status))
    # print(b.json())
