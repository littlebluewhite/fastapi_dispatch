import datetime
from pydantic import BaseModel


class Test(BaseModel):
    time: datetime.datetime
    timedelta: datetime.timedelta
    name: str


if __name__ == "__main__":
    a = Test(timedelta=10, name="aa", time="2022-1-11 11:00:02.444")
    print(a)
    # print(type(datetime.timedelta(seconds=120).seconds))
    # b = Test(**a.dict())
    # print(b)
