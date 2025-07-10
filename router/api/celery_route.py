from fastapi import APIRouter,Depends,status,File,UploadFile,BackgroundTasks
from config.celery_app import celeryapp
from celery.result import AsyncResult
from validation.emp_m import EmpSchemaOut
from core.auth import getCurrentActiveEmp
from typing import Annotated

router = APIRouter()

@router.post("/tasks_a/")
def run_task(
    current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],
    x:int,
    y:int,
    z:int
    ):
    task = celeryapp.send_task("celery_tasks.arithmetic.add", args=[x, y,z])
    return {"task_id": task.id}

 
@router.get("/tasks_a/{task_id}")
def get_task_result(current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],task_id: str):
    result = AsyncResult(task_id, app=celeryapp)
    return {"task_id": task_id, "status": result.status, "result": result.result}

# create separate endpoint to get result.
# celery task is asynchronous. If you fetch result in same function then it give None or PENDING because task started execution just.
@router.post("/tasks_c/")
def add_data(current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],x:int, y:int, z:int):
    task = celeryapp.send_task("celery_tasks.arithmetic.add", args=[x, y,z])
    task_id = task.id
    result = AsyncResult(task_id, app=celeryapp)
    return {"task_id": task_id, "status": result.status, "result": result.result}


@router.post("/tasks_m/")
def run_task(current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],x:int, y:int, z:int):
    task = celeryapp.send_task("celery_tasks.arithmetic.add", args=[x, y,z])
    return {"task_id": task.id}

 
@router.get("/tasks_n/{task_id}")
def get_task_result(current_user: Annotated[EmpSchemaOut, Depends(getCurrentActiveEmp)],task_id: str):
    result = AsyncResult(task_id, app=celeryapp)
    return {"task_id": task_id, "status": result.status, "result": result.result}
