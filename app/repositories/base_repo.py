from uuid import UUID
from typing import Type, TypeVar, Generic
from pydantic import BaseModel
from sqlmodel.sql.expression import SelectOfScalar
from sqlmodel import SQLModel, Session, select, func

T = TypeVar("T", bound=SQLModel)


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_all(self) -> list[T]:
        return list(self.db.exec(select(self.model)).all())

    def get(self, id: UUID | str | int) -> T | None:
        return self.db.get(self.model, id)

    def add(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, id: UUID | str | int) -> bool:
        db_obj = self.get(id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True

    def paginate(
        self,
        query: SelectOfScalar[T],
        *,
        page: int = 1,
        size: int = 10,
    ) -> Page[T]:
        page = max(page, 1)
        size = max(size, 1)
        offset = (page - 1) * size

        total = self.db.exec(select(func.count()).select_from(query.subquery())).one()

        items = self.db.exec(query.offset(offset).limit(size)).all()

        return Page[T](
            items=list(items),
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )
