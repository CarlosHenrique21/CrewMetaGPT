from app.repositories.task_repository import TaskRepository
from app.models.task import Task
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

class TaskService:
    def __init__(self, session: AsyncSession):
        self.repo = TaskRepository(session)

    async def create_task(self, task: Task) -> Task:
        return await self.repo.create(task)

    async def get_task(self, task_id: UUID) -> Optional[Task]:
        return await self.repo.get_by_id(task_id)

    async def update_task(self, task_id: UUID, **kwargs) -> Optional[Task]:
        return await self.repo.update(task_id, **kwargs)

    async def delete_task(self, task_id: UUID) -> bool:
        return await self.repo.delete(task_id)

    async def list_tasks(self, user_id: UUID, filters: dict, offset: int=0, limit: int=10, order_by: str='due_date', order_desc: bool=False) -> List[Task]:
        return await self.repo.list(user_id, filters, offset, limit, order_by, order_desc)
