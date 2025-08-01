from fastapi import APIRouter, FastAPI
from router.api import test_route
from router.api import cs_g_m_route
from router.api import cs_m_route
from router.api import emp_route
from router.api import auth_route
from router.api import celery_route

api_router = APIRouter()
api_router.include_router(auth_route.router, prefix="", tags=["Login"])
api_router.include_router(test_route.router, prefix="", tags=["Test"])
api_router.include_router(cs_g_m_route.router, prefix="", tags=["cs_g_m"])
api_router.include_router(cs_m_route.router, prefix="", tags=["cs_m"])
api_router.include_router(emp_route.router, prefix="", tags=["Registration"])
api_router.include_router(celery_route.router, prefix="", tags=["Celery Test"])
