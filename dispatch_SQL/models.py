import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Interval, DateTime, Enum, \
    Text, LargeBinary
from sqlalchemy.orm import relationship
from dispatch_SQL.database import Base
from dispatch_data.enum_data import ReplyConfirmStatus, ReplyFileType


class DispatchTask(Base):
    __tablename__ = "dispatch_task"

    id = Column(Integer, primary_key=True, index=True)
    dispatch_event_id = Column(String(64), unique=True)
    bind_event_id = Column(String(64))
    category = Column(String(64))
    level_id = Column(Integer, ForeignKey("dispatch_level.id"))
    provider = Column(String(64))
    job = Column(String(64))
    location = Column(String(64))
    assign_account = Column(JSON)
    assign_account_role = Column(JSON)
    assign_account_group = Column(JSON)
    people_limit = Column(Integer)
    order_taker = Column(JSON)
    deadline = Column(DateTime)
    ack_method_id = Column(Integer, ForeignKey("dispatch_ack_method.id"))
    status_id = Column(Integer, ForeignKey("dispatch_status.id"))
    isActive = Column(Boolean, default=True, nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    end_time = Column(DateTime, nullable=True)

    level = relationship("DispatchLevel", back_populates="task")
    ack_method = relationship("DispatchAckMethod", back_populates="task")
    status = relationship("DispatchStatus", back_populates="task")

    reply = relationship("DispatchReply", back_populates="task", lazy="immediate")
    confirm = relationship("DispatchConfirm", back_populates="task", lazy="immediate")


class DispatchReply(Base):
    __tablename__ = "dispatch_reply"

    id = Column(Integer, primary_key=True, index=True)
    dispatch_task_id = Column(Integer, ForeignKey("dispatch_task.id"))
    worker_name = Column(String(64))
    status = Column(Enum(ReplyConfirmStatus))
    description = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

    file = relationship("DispatchReplyFile", back_populates="reply", lazy="immediate")

    task = relationship("DispatchTask", back_populates="reply")


class DispatchReplyFile(Base):
    __tablename__ = "dispatch_reply_file"

    id = Column(Integer, primary_key=True, index=True)
    dispatch_reply_id = Column(Integer, ForeignKey("dispatch_reply.id"))
    filename = Column(String(64))
    file_type = Column(Enum(ReplyFileType))
    content_type = Column(String(64))
    data = Column(LargeBinary(length=(2**32)-1))

    reply = relationship("DispatchReply", back_populates="file")


class DispatchConfirm(Base):
    __tablename__ = "dispatch_confirm"

    id = Column(Integer, primary_key=True, index=True)
    dispatch_task_id = Column(Integer, ForeignKey("dispatch_task.id"))
    provider_name = Column(String(64))
    status = Column(Enum(ReplyConfirmStatus))
    description = Column(Text)
    create_time = Column(DateTime, default=datetime.datetime.now)

    task = relationship("DispatchTask", back_populates="confirm")


class DispatchStatus(Base):
    __tablename__ = "dispatch_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    description = Column(String(64))

    task = relationship("DispatchTask", back_populates="status")


class DispatchLevel(Base):
    __tablename__ = "dispatch_level"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    description = Column(String(64))
    color_code = Column(JSON)

    task = relationship("DispatchTask", back_populates="level")
    template = relationship("DispatchTemplate", back_populates="level")


class DispatchAckMethod(Base):
    __tablename__ = "dispatch_ack_method"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    description = Column(String(64))
    need_text = Column(Boolean, default=False)
    need_photo = Column(Boolean, default=False)
    need_video = Column(Boolean, default=False)

    task = relationship("DispatchTask", back_populates="ack_method")
    template = relationship("DispatchTemplate", back_populates="ack_method")


class DispatchTemplate(Base):
    __tablename__ = "dispatch_template"

    id = Column(Integer, primary_key=True, index=True)
    dependence = Column(String(64))
    category = Column(String(64))
    level_id = Column(Integer, ForeignKey("dispatch_level.id"))
    job = Column(String(64))
    location = Column(String(64))
    assign_account_role = Column(JSON)
    assign_account_group = Column(JSON)
    people_limit = Column(Integer)
    time_limit = Column(Interval)
    ack_method_id = Column(Integer, ForeignKey("dispatch_ack_method.id"))
    modify_time = Column(DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)

    level = relationship("DispatchLevel", back_populates="template")
    ack_method = relationship("DispatchAckMethod", back_populates="template")
