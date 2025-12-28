import uuid
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params
from sqlmodel import Session, col, select, asc, desc
from app.core.constants import RoleEnum
from app.core.security import hash_password
from app.models.user import User
from app.repositories.base_repo import BaseRepository
from app.repositories.role_repo import RoleRepository
from app.schemas.user import UserCreateRequest, UserSearchRequest, UserUpdateRequest


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
        self.role_repo = RoleRepository(db)

    def get_by_username(self, username: str) -> User | None:
        return self.db.exec(select(User).where(User.username == username)).first()

    def create(self, user_in: UserCreateRequest) -> User:
        default_role = self.role_repo.get_by_name(RoleEnum.USER.value)

        user = User(
            username=user_in.username,
            password_hash=hash_password(user_in.password),
            role_id=default_role.id if default_role else None,
        )
        return self.add(user)

    def update(self, user_id: uuid.UUID, user_in: UserUpdateRequest) -> User | None:
        user = self.get(user_id)
        if not user:
            return None
        if user_in.username is not None:
            user.username = user_in.username
        if user_in.password is not None:
            user.password_hash = hash_password(user_in.password)
        if user_in.role_id is not None:
            user.role_id = user_in.role_id
        return self.add(user)

    def update_role(self, user_id: uuid.UUID, role_name: RoleEnum) -> User | None:
        user = self.get(user_id)
        if not user:
            return None

        role = self.role_repo.get_by_name(role_name)
        if not role:
            return None

        user.role_id = role.id
        return self.add(user)

    def search(self, params: UserSearchRequest) -> dict:
        # init query select
        query = select(User)

        # Handle Search
        if params.search:
            query = query.where(col(User.username).ilike(f"%{params.search}%"))

        # Handle Filter
        if params.filter:
            for field, value in params.filter.items():
                attr = getattr(User, field, None)
                if attr is not None and value is not None:
                    query = query.where(attr == value)

        # Handle Sort
        sort_field = params.sort_by or "username"
        sort_order = params.sort_order or "asc"
        sort_column = getattr(User, sort_field, User.username)
        query = query.order_by(
            desc(sort_column) if sort_order == "desc" else asc(sort_column)
        )

        # Handle Paging
        result = self.paginate(query, page=params.page, size=params.size)

        return {
            **vars(result),
            "sort_by": sort_field,
            "sort_order": sort_order,
            "filter": params.filter,
        }

    # def search(self, params: UserSearchRequest):
    #     # 1. Init query select
    #     query = select(User)

    #     # 2. Handle Search
    #     if params.search:
    #         query = query.where(col(User.username).ilike(f"%{params.search}%"))

    #     # 3. Handle Filter
    #     if params.filter:
    #         for field, value in params.filter.items():
    #             attr = getattr(User, field, None)
    #             if attr is not None and value is not None:
    #                 query = query.where(attr == value)

    #     # 4. Handle Sort
    #     sort_field = params.sort_by or "username"
    #     sort_order = params.sort_order or "asc"
    #     sort_column = getattr(User, sort_field, User.username)

    #     query = query.order_by(
    #         desc(sort_column) if sort_order == "desc" else asc(sort_column)
    #     )

    #     page_data = paginate(self.db, query, Params(page=params.page, size=params.size))

    #     return {
    #         **page_data.model_dump(),
    #         "filter": params.filter,
    #         "sort_by": params.sort_by,
    #         "sort_order": params.sort_order,
    #     }
