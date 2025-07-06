from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, status, Request, BackgroundTasks
from fastapi import APIRouter
from sqlalchemy.orm import Session
from validation.auth import (AuthCredentialIn,AuthOut, Logout,Status422Response,Status400Response,Status401Response)
from fastapi.responses import JSONResponse, ORJSONResponse
from database.session import get_db
from config.logconfig import loglogger
from core.auth import authenticate
from core.token import create_access_token
from config.loadenv import envconst
from config.message import auth_message
from config.message import logout_message
from validation.email import EmailSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
from config.fastapi_mail_config import send_email, mailconf
from config.redis_session import redisSessionObj
from core.auth import getCurrentActiveEmp
from core.httpbearer import get_api_token
from core.httpbearer import http_bearer
from config.constants import constants
from database.model_functions.login import get_emp_for_login
from validation.emp_m import EmpSchemaOut
from exception.custom_exception import CustomException

router = APIRouter()

@router.post(
    "/login",
    response_model=AuthOut,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": Status422Response},
        status.HTTP_400_BAD_REQUEST: {"model": Status400Response},
        status.HTTP_401_UNAUTHORIZED: {"model": Status401Response}
    },
    name="login"
    )

async def login(
    background_tasks: BackgroundTasks,
    credentials:AuthCredentialIn,
    db:Session = Depends(get_db)
    ):
    AuthCredentialIn.check_email_exist(db,credentials.email)
    authemp = authenticate(credentials.email, credentials.password, db)
    try:
        access_token_expires = timedelta(minutes=int(envconst.ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
        data={"email": authemp.email}, expires_delta=access_token_expires
    )
        http_status_code = status.HTTP_200_OK
        datalist = list()
        datadict = {}
        datadict['id'] = authemp.id
        datadict['emp_name'] = authemp.emp_name
        datadict['email'] = authemp.email
        datadict['status'] = authemp.status
        datadict['mobile'] = authemp.mobile
        datalist.append(datadict)

        loginuserdict = {}
        loginuserdict['id'] = authemp.id
        loginuserdict['emp_name'] = authemp.emp_name
        loginuserdict['email'] = authemp.email
        loginuserdict['status'] = authemp.status

        redisSessionObj.set_session(authemp.id,"loginuser", loginuserdict)

        response_dict = {
            "status_code": http_status_code,
            "status":True,
            "message":auth_message.AUTH_SUCCESSFULL,
            "token_type":envconst.TOKEN_TYPE,
            "access_token":access_token,
            "data":datalist
        }
        response_data = AuthOut(**response_dict) 
        response = JSONResponse(content=response_data.model_dump(),status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(response_data.model_dump()))

        body = """<h1>Your have successfully Test</h1> """
        subject = "Your have successfully login"
        toemail = [authemp.email]
        ccemail = ['atulcc@yopmail.com']
        bccemail = ['atulbcc@yopmail.com']
        emailBody = body
        send_email(background_tasks=background_tasks,emaiSubject=subject,emailTo=toemail,emailBody=emailBody,ccemail=ccemail,bccemail=bccemail)
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":"Type:"+str(type(e))+", Message:"+str(e)
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response
    
@router.post("/logout", response_model=Logout)
async def logout(current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)], db:Session = Depends(get_db)):
    try:
        loginuserid = current_user.id
        if loginuserid is None:
            raise CustomException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                status=False,
                message=auth_message.LOGIN_REQUIRED,
                data=[]
            )
        redisSessionObj.delete_all_session(loginuserid)
        http_status_code: int = status.HTTP_200_OK
        status_ok:bool = constants.STATUS_OK
        data={"status_code":http_status_code,"status":status_ok,"message":logout_message.LOGOT_SUCCESS}
        response_data = Logout(**data)
        response = JSONResponse(content=response_data.model_dump(),status_code=http_status_code)
        return response
    except Exception as e:
        http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {
            "status_code": http_status_code,
            "status":False,
            "message":"Type:"+str(type(e))+", Message:"+str(e)
        }
        response = JSONResponse(content=data,status_code=http_status_code)
        loglogger.debug("RESPONSE:"+str(data))
        return response