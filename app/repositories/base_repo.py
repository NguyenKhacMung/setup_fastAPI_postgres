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

    def get_by_id(self, id: UUID | str | int) -> T | None:
        return self.db.get(self.model, id)

    def add(self, db_obj: T) -> T:
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def create(self, data: BaseModel, extra_data: dict | None = None) -> T:
        obj = self.model.model_validate(data, update=extra_data)
        return self.add(obj)

    def update_by_id(
        self,
        id: UUID | str | int,
        data: BaseModel | dict,
        extra_data: dict | None = None,
    ) -> T | None:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        update_data = (
            data.model_dump(exclude_unset=True)
            if isinstance(data, BaseModel)
            else dict(data)
        )

        db_obj.sqlmodel_update(update_data, update=extra_data)

        return self.add(db_obj)

    def delete_by_id(self, id: UUID | str | int) -> bool:
        db_obj = self.get_by_id(id)
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
