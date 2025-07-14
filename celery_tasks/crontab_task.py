from config.celery_app import celeryapp
from config.celery_mail_config import mailconf
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr
from validation.email import EmailSchema
import os
import asyncio

@celeryapp.task(name="celery_tasks.crontab_task.send_email_by_cron")
def send_email_task():
    body = """<h1>Your have successfully test celery crontab 2</h1> """
    subject = "Your have successfully login"
    toemail = ['atulcron@yopmail.com']
    ccemail = ['atulccc@yopmail.com']
    bccemail = ['atulbcc@yopmail.com']
    emailBody = body
    attachmentsList = []
    mailData = MessageSchema(
        subject=subject,
        recipients=toemail,
        cc=ccemail,
        bcc=bccemail,
        body=emailBody,
        subtype=MessageType.html,
        attachments=attachmentsList
        )
    fm = FastMail(mailconf)
    asyncio.run(fm.send_message(mailData))