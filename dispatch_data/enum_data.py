import enum


class ReplyConfirmStatus(enum.Enum):
    fail = "fail"
    success = "success"
    other = "other"


class ReplyFileType(enum.Enum):
    photo = "photo"
    video = "video"
