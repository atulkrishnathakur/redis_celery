from database.model.emp_m import Empm
from fastapi import Depends, status
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import func
from core.hashing import HashData
from config.constants import constants
from database.dbconnection import engine
from config.logconfig import loglogger
from fastapi.responses import JSONResponse, ORJSONResponse

def get_emp_for_login(db,email):
    try:
        stmt = select(Empm).where(Empm.email == email).where(Empm.status == 1)
        result = db.execute(stmt)
        data = result.scalars().first()
        return data
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":str(e)
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response
