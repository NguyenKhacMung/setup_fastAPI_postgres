from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    USER = "User"


class PermissionEnum(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
