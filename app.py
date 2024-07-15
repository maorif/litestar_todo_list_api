from litestar import Litestar, get, post, delete, put
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.contrib.sqlalchemy.plugins import (
    SQLAlchemySerializationPlugin,
    SQLAlchemyPlugin,
)

from domain import TodoItem
from db_adapter import (
    provide_transaction,
    get_todo_list,
    get_todo_by_title,
    delete_todo_by_title,
    db_config,
)


@get("/")
def hello_world() -> str:
    return "Hello, World!"


@post("/todo_list")
async def add_item(data: TodoItem, transaction: AsyncSession) -> TodoItem:
    transaction.add(data)
    return data


@get("/todo_list")
async def get_list(
    transaction: AsyncSession, done: bool | None = None
) -> list[TodoItem]:
    return await get_todo_list(done, transaction)


@put("/todo_list/{title:str}")
async def update_item(
    title: str, data: TodoItem, transaction: AsyncSession
) -> TodoItem:
    todo_item = await get_todo_by_title(title=title, session=transaction)
    todo_item.title = data.title
    todo_item.done = data.done
    return todo_item


@delete("/todo_list/{title:str}")
async def remove_item(title: str, transaction: AsyncSession) -> None:
    await delete_todo_by_title(title=title, session=transaction)
    return


app = Litestar(
    [hello_world, add_item, get_list, update_item, remove_item],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemySerializationPlugin(), SQLAlchemyPlugin(config=db_config)],
)
