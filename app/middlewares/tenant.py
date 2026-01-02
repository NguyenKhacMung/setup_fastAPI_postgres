from starlette.middleware.base import BaseHTTPMiddleware
from app.core.tenant import set_schema


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tenant_id = request.headers.get("X-TENANT-ID")

        if tenant_id:
            set_schema(f"tenant_{tenant_id}")

        return await call_next(request)
