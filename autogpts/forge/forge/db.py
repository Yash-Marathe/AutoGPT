from .sdk import AgentDB, ForgeLogger, NotFoundError, Base
from sqlalchemy.exc import SQLAlchemyError

import datetime
from sqlalchemy import (
    Column,
    DateTime,
    String,
)

LOG = ForgeLogger(__name__)


class ChatModel(Base):
    __tablename__ = "chat"
    msg_id = Column(String, primary_key=True, index=True)
    task_id = Column(String)
    role = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class ActionModel(Base):
    __tablename__ = "action"
    action_id = Column(String, primary_key=True, index=True)
    task_id = Column(String)
    name = Column(String)
    args = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )


class ForgeDatabase(AgentDB):
    def __init__(self, debug_enabled: bool):
        self.debug_enabled = debug_enabled

    async def log_and_handle_sql_alchemy_error(self, func):
        """
        A helper function to log SQLAlchemy errors and re-raise them.
        """
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except SQLAlchemyError as e:
                LOG.error(f"SQLAlchemy error in {func.__name__}: {e}")
                raise
        return wrapper

    async def log_and_handle_not_found_error(self, func):
        """
        A helper function to log NotFoundErrors and re-raise them.
        """
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except NotFoundError as e:
                LOG.error(f"NotFoundError in {func.__name__}: {e}")
                raise
        return wrapper

    @log_and_handle_sql_alchemy_error
    async def add_chat_history(self, task_id: str, messages: list):
        for message in messages:
            await self.add_chat_message(task_id, message["role"], message["content"])

    @log_and_handle_sql_alchemy_error
    @log_and_handle_not_found_error
    async def add_chat_message(self, task_id: str, role: str, content: str):
        if self.debug_enabled:
            LOG.debug("Creating new task")
        with self.Session() as session:
            mew_msg = ChatModel(
                msg_id=str(uuid.uuid4()),
                task_id=task_id,
                role=role,
                content=content,
            )
            session.add(mew_msg)
            session.commit()
            session.refresh(mew_msg)
            if self.debug_enabled:
                LOG.debug(f"Created new Chat message with task_id: {mew_msg.msg_id}")
            return mew_msg

    @log_and_handle_sql_alchemy_error
    @log_and_handle_not_found_error
    async def get_chat_history(self, task_id: str):
        if self.debug_enabled:
            LOG.debug(f"Getting chat history with task_id: {task_id}")
        with self.Session() as session:
            messages = (
                session.query(ChatModel)
                .filter(ChatModel.task_id == task_id)
                .order_by(ChatModel.created_at)
                .all()
            )
            if messages:
                return [{"role": m.role, "content": m.content} for m in messages]
            else:
                LOG.error(f"Chat history not found with task_id: {task_id}")
                raise NotFoundError("Chat history not found")

    @log_and_handle_sql_alchemy_error
    async def create_action(self, task_id: str, name: str, args: str):
        with self.Session() as session:
            new_action = ActionModel(
                action_id=str(uuid.uuid4()),
                task_id=task_id,
                name=name,
                args=args,
            )
            session.add(new_action)
            session.commit()
            session.refresh(new_action)
            if self.debug_enabled:
                LOG.debug(
                    f"Created new Action with task_id: {new_action.action_id}"
                )
            return new_action

    @log_and_handle_sql_alchemy_error
    @log_and_handle_not_found_error
    async def get_action_history(self, task_id: str):
        if self.debug_enabled:
            LOG.debug(f"Getting action history with task_id: {task_id}")
        with self.Session() as session:
            actions = (
                session.query(ActionModel)
                .filter(ActionModel.task_id == task_id)
                .order_by(ActionModel.
