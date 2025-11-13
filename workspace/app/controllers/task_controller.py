from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse, StatusEnum, PriorityEnum
from app.services.task_service import TaskService
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from typing import List, Optional
from uuid import UUID

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.post('', response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    from app.models.task import Task
    new_task = Task(
        user_id=current_user.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date
    )
    created_task = await task_service.create_task(new_task)
    return created_task

@router.get('', response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[StatusEnum] = Query(None),
    priority: Optional[PriorityEnum] = Query(None),
    due_date: Optional[str] = Query(None),
    page: int = 1,
    page_size: int = 10,
    order_by: str = 'due_date',
    order_desc: bool = False,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    filters = {}
    if status:
        filters['status'] = status
    if priority:
        filters['priority'] = priority
    if due_date:
        filters['due_date'] = due_date
    offset = (page - 1) * page_size
    tasks = await task_service.list_tasks(current_user.id, filters, offset, page_size, order_by, order_desc)
    return tasks

@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put('/{task_id}', response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    existing_task = await task_service.get_task(task_id)
    if not existing_task or existing_task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated_task = await task_service.update_task(task_id, **task_update.dict(exclude_unset=True))
    return updated_task

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    task_service = TaskService(db)
    existing_task = await task_service.get_task(task_id)
    if not existing_task or existing_task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    deleted = await task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete task")
    return
