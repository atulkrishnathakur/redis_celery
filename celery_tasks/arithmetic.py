from config.celery_app import celeryapp

@celeryapp.task(name="celery_tasks.arithmetic.add")  # Explicitly naming the task
def add(x, y, z):
    return x + y + z
