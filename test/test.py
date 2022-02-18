from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from dispatch_main import dispatch_app

client = TestClient(dispatch_app)


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_read_dispatch():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {}
