from config.celery_app import celeryapp
from config.celery_mail_config import mailconf
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr
from validation.email import EmailSchema
import os
import asyncio

@celeryapp.task(name="celery_tasks.email.send_email_task")
def send_email_task(emaiSubject, emailTo, emailBody, ccemail=[], bccemail=[],attachmentsList=[]):
    mailData = MessageSchema(
        subject=emaiSubject,
        recipients=emailTo,
        cc=ccemail,
        bcc=bccemail,
        body=emailBody,
        subtype=MessageType.html,
        attachments=attachmentsList
        )
    fm = FastMail(mailconf)
    asyncio.run(fm.send_message(mailData))