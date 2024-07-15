from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


TodoType = dict[str, Any]
TodoCollectionType = list[TodoType]


class Base(DeclarativeBase): ...


class TodoItem(Base):
    __tablename__ = "todo_items"

    title: Mapped[str] = mapped_column(primary_key=True)
    done: Mapped[bool]


def serialize_todo(todo: TodoItem) -> TodoType:
    return {"title": todo.title, "done": todo.done}
