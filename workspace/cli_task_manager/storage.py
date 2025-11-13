import os
import sqlite3
from sqlite3 import Connection
from typing import Optional, List
from datetime import datetime
from cli_task_manager.models import Task

DB_DIR = os.path.join(os.path.expanduser('~'), '.cli_task_manager')
DB_PATH = os.path.join(DB_DIR, 'tasks.db')

class Storage:
    def __init__(self):
        os.makedirs(DB_DIR, exist_ok=True)
        self.conn: Connection = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          description TEXT NOT NULL,
          status TEXT CHECK(status IN ('pending','done')) NOT NULL DEFAULT 'pending',
          priority INTEGER,
          due_date DATE,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          completed_at TIMESTAMP
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, description: str, priority: Optional[int] = None, due_date: Optional[str] = None) -> int:
        query = '''INSERT INTO tasks (description, priority, due_date) VALUES (?, ?, ?)'''
        cur = self.conn.cursor()
        cur.execute(query, (description, priority, due_date))
        self.conn.commit()
        return cur.lastrowid

    def get_tasks(self) -> List[Task]:
        query = '''SELECT * FROM tasks ORDER BY id ASC'''
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            due_date = None
            if row['due_date']:
                try:
                    due_date = datetime.strptime(row['due_date'], '%Y-%m-%d')
                except ValueError:
                    due_date = None
            completed_at = None
            if row['completed_at']:
                try:
                    completed_at = datetime.strptime(row['completed_at'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    completed_at = None
            task = Task(
                id=row['id'],
                description=row['description'],
                status=row['status'],
                priority=row['priority'],
                due_date=due_date,
                created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S'),
                completed_at=completed_at
            )
            tasks.append(task)
        return tasks

    def mark_done(self, task_id: int) -> bool:
        query = '''UPDATE tasks SET status='done', completed_at=CURRENT_TIMESTAMP WHERE id=? AND status='pending' '''
        cur = self.conn.cursor()
        cur.execute(query, (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        query = '''DELETE FROM tasks WHERE id=?'''
        cur = self.conn.cursor()
        cur.execute(query, (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()
