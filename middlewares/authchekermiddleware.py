from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse, ORJSONResponse, HTMLResponse
from fastapi import Depends, status, HTTPException, Request, Header
from router.router_base import api_router
from exception.custom_exception import CustomException
from config.message import auth_message
import re
from core.auth import getCurrentEmp,getCurrentActiveEmp
from database.session import get_db
import jwt
from config.loadenv import envconst
from validation.auth import TokenData


# https://fastapi.tiangolo.com/tutorial/middleware/

class AuthCheckerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, some_attribute: str):
        super().__init__(app)
        self.some_attribute = some_attribute
    # url_path_for("route name here")
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        excluded_paths = [
            "/redis_celery-docs",
            "/api/redis_celery.json",
            "/api"+api_router.url_path_for("login"),
            "/api"+api_router.url_path_for("apitest"),
            "/api/uploads/.*",
            "/api/pdf/.*"
            ]
        
        if any(re.match(path, request.url.path) for path in excluded_paths):
            return await call_next(request)

        # Validate token
        if not token or not token.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status_code":status.HTTP_401_UNAUTHORIZED,
                    "status":False,
                    "message":auth_message.LOGIN_REQUIRED,
                    "data":[]
                    },
            )
        token_value = token.split(" ")[1]  # Get the part after "Bearer"
        if not token_value:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "status_code":status.HTTP_401_UNAUTHORIZED,
                    "status":False,
                    "message":auth_message.LOGIN_REQUIRED,
                    "data":[]
                    },
            )

        payload = jwt.decode(token_value, envconst.SECRET_KEY, algorithms=[envconst.ALGORITHM])
        return await call_next(request)
