from celery import Celery
from core.celery_crontab_schedule import beat_schedule_task

celeryapp = Celery(
    "celerybrocker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celeryapp.conf.timezone = 'Asia/Kolkata'

celeryapp.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    #include=["app.tasks"]  # Autodiscovery of tasks
    include=["celery_tasks.arithmetic","celery_tasks.email","celery_tasks.crontab_task"]  # Autodiscovery of tasks
)

celeryapp.conf.beat_schedule = beat_schedule_task