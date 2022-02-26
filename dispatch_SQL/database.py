from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dispatch_config import dispatch_config

sql_config = dispatch_config()["Dispatch_Database"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{sql_config['user']}:{sql_config['password']}" \
                          f"@{sql_config['host']}:{sql_config['port']}/{sql_config['db']}"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/dispatch"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


if __name__ == "__main__":
    # a = SessionLocal().execute('''select id from dispatch_task where json_search(json_extract(
    #     order_taker, '$[*]'),'all', "RR") is not null and ack_method_id in ("3")''').all()

    a = SessionLocal().execute('''select id from dispatch_task where start_time <= "2022-02-25T14:14:00Z"''').all()

    print(a)
    # c = (i[0] for i in a)
    # a = a.all()
    # print(a)
    # b = SessionLocal().query(models.DispatchTask).filter(models.DispatchTask.id.in_(c),
    #                                                      models.DispatchTask.ack_method_id == 3).all()
    # print(jsonable_encoder(b))
    # print(jsonable_encoder(b, custom_encoder={
    #         bytes: lambda v: base64.b64encode(v).decode('utf-8')}))
    # print(type(SessionLocal()))
    # for i in a:
    #     print(i)
    pass
