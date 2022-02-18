from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dispatch_config import dispatch_config

sql_config = dispatch_config()["Dispatch_Database"]
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{sql_config['user']}:{sql_config['password']}" \
                          f"@{sql_config['host']}:{sql_config['port']}/{sql_config['db']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
