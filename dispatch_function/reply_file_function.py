import os
import random

import aiofiles as aiofiles
from fastapi import UploadFile
from dispatch_exception import DispatchException


def file_generator(path: str):
    with open(path, mode="rb") as f:
        yield from f


async def write_reply_file(file: UploadFile, reply_id):
    path = f"./static/reply_file/{str(reply_id)}_{int(random.random()*1000)}_{file.filename.replace(' ', '_')}"
    async with aiofiles.open(path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return path


def delete_reply_file(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        raise DispatchException(status_code=502, detail="server remove file error")
