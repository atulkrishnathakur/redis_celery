
from celery.schedules import crontab 

beat_schedule_task = {
    'send-email': {
        'task': 'celery_tasks.crontab_task.send_email_by_cron',
        'schedule': crontab(),  # Every Minute
        'args': ()
    },
}