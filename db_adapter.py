from collections.abc import AsyncGenerator

from litestar.exceptions import ClientException, NotFoundException
from litestar.status_codes import HTTP_409_CONFLICT

from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig

from domain import Base, TodoItem
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PSWD, POSTGRES_USER


CON_STR = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PSWD}@{POSTGRES_HOST}/{POSTGRES_DB}"

db_config = SQLAlchemyAsyncConfig(
    connection_string=CON_STR,
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)


async def provide_transaction(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


async def get_todo_list(done: bool | None, session: AsyncSession) -> list[TodoItem]:
    query = select(TodoItem)
    if done is not None:
        query = query.where(TodoItem.done.is_(done))

    result = await session.execute(query)
    return result.scalars().all()


async def get_todo_by_title(title: str, session: AsyncSession):
    query = select(TodoItem).where(TodoItem.title == title)
    result = await session.execute(query)
    try:
        return result.scalar_one()
    except NoResultFound as e:
        raise NotFoundException(detail=f"TODO {title!r} not found") from e


async def delete_todo_by_title(title: str, session: AsyncSession) -> None:
    query = delete(TodoItem).where(TodoItem.title == title)
    result = await session.execute(query)
    try:
        print(result)
        return result
    except NoResultFound as e:
        raise NotFoundException(detail=f"TODO {title!r} not found") from e
