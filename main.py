from fastapi import FastAPI
from fastapi import FastAPI,Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from router.router_base import api_router
from router.web_router_base import web_router
from exception.custom_exception import CustomException,unicorn_exception_handler
from middlewares.authchekermiddleware import AuthCheckerMiddleware
from config.static_mount import mount_uploaded_files, mount_generated_pdf

def include_router(app):
    app.include_router(api_router)
    app.include_router(web_router)

def start_application():
    app = FastAPI(
        DEBUG=True,
        title="softbook",
        summary="This is a fastapi project",
        description="This is fastapi project with sqlalchemy",
        version="1.0.0",
        openapi_url="/softbook.json",
        docs_url="/softbook-docs",
        redoc_url="/softbook-redoc",
        root_path="/api",
        root_path_in_servers=True,
        )
        
    mount_uploaded_files(app)
    mount_generated_pdf(app)    
    include_router(app)
    return app

app = start_application()
app.add_exception_handler(CustomException,unicorn_exception_handler)
app.add_middleware(AuthCheckerMiddleware, some_attribute="example_attribute")
