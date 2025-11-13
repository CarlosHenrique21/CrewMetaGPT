from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.task import Task
from typing import List, Optional
from uuid import UUID

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: UUID) -> Optional[Task]:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalars().first()

    async def update(self, task_id: UUID, **kwargs) -> Optional[Task]:
        await self.session.execute(update(Task).where(Task.id == task_id).values(**kwargs))
        await self.session.commit()
        return await self.get_by_id(task_id)

    async def delete(self, task_id: UUID) -> bool:
        result = await self.session.execute(delete(Task).where(Task.id == task_id))
        await self.session.commit()
        return result.rowcount > 0

    async def list(self, user_id: UUID, filters: dict, offset: int = 0, limit: int = 10, order_by: str = 'due_date', order_desc: bool = False) -> List[Task]:
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if 'status' in filters:
            query = query.where(Task.status == filters['status'])
        if 'priority' in filters:
            query = query.where(Task.priority == filters['priority'])
        if 'due_date' in filters:
            query = query.where(Task.due_date == filters['due_date'])

        # Ordering
        order_column = getattr(Task, order_by, Task.due_date)
        if order_desc:
            order_column = order_column.desc()
        else:
            order_column = order_column.asc()

        query = query.order_by(order_column).offset(offset).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()
