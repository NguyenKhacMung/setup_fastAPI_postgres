from typing import Generic, Type, TypeVar
from sqlmodel import Session, SQLModel, select, func, col, asc, desc

from app.schemas.base import PagingRequest

# Khai báo biến Generic T dựa trên SQLModel
T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def paginate(self, params: PagingRequest, search_field: str = "name") -> dict:
        # 1. Init query select
        query = select(self.model)

        # 2. Handle Search (search_field)
        if params.search:
            search_attr = getattr(self.model, search_field, None)
            if search_attr is not None:
                query = query.where(col(search_attr).ilike(f"%{params.search}%"))

        # 3. handle Filter
        applied_filters = {}
        if params.filter:
            for field, value in params.filter.items():
                attr = getattr(self.model, field, None)
                if attr is not None and value is not None:
                    query = query.where(attr == value)
                    applied_filters[field] = value

        # 4. Count Total
        total = self.db.exec(select(func.count()).select_from(query.subquery())).one()

        # 5. Handle Sort
        sort_field = params.sort_by or search_field
        sort_order = params.sort_order or "asc"

        sort_column = getattr(self.model, sort_field, None)
        if sort_column is not None:
            query = query.order_by(
                desc(sort_column) if sort_order == "desc" else asc(sort_column)
            )

        # 6. Handle Paging
        page = max(params.page, 1)
        page_size = max(params.size, 1)
        offset = (page - 1) * page_size

        results = self.db.exec(query.offset(offset).limit(page_size)).all()

        return {
            "items": results,
            "total_items": total,
            "total_pages": (total + page_size - 1) // page_size,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_field,
            "sort_order": sort_order,
            "filter": applied_filters,
        }
