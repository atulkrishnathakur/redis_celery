from celery import Celery

celeryapp = Celery(
    "celerybrocker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celeryapp.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
    #include=["app.tasks"]  # Autodiscovery of tasks
    include=["celery_tasks.arithmetic","celery_tasks.email"]  # Autodiscovery of tasks
)