from loguru import logger
from fastapi import Request


async def log_request(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
