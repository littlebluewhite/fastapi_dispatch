import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from dispatch_SQL import models
from dispatch_SQL.database import engine
from dispatch_exception import DispatchException
from dispatch_redis.redis import redisDB
from routers import dispatch_task, dispatch_reply, dispatch_confirm, dispatch_status, dispatch_level, \
    dispatch_ack_method, dispatch_template, client_api, dispatch_reply_file

dispatch_app = FastAPI(title="dispatch_app")

dispatch_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# redis
redis = redisDB

# SQL DB
#   create SQL models
models.Base.metadata.create_all(bind=engine)

# router
dispatch_app.include_router(dispatch_task.router)
dispatch_app.include_router(dispatch_reply.router)
dispatch_app.include_router(dispatch_reply_file.router)
dispatch_app.include_router(dispatch_confirm.router)
dispatch_app.include_router(dispatch_status.router)
dispatch_app.include_router(dispatch_level.router)
dispatch_app.include_router(dispatch_ack_method.router)
dispatch_app.include_router(dispatch_template.router)
dispatch_app.include_router(client_api.router)


@dispatch_app.exception_handler(DispatchException)
async def unicorn_exception_handler(request: Request, exc: DispatchException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.detail}"},
    )


@dispatch_app.get("/exception")
async def test_exception():
    raise DispatchException(status_code=423, detail="test exception")


if __name__ == "__main__":
    uvicorn.run(dispatch_app, host='0.0.0.0', port=9800,
                log_level="info", limit_concurrency=400)
