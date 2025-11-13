import argparse
from src.task_manager import TaskManager

class CLICommandParser:
    def __init__(self):
        self.task_manager = TaskManager()
        self.parser = argparse.ArgumentParser(description='CLI Task Manager')
        subparsers = self.parser.add_subparsers(dest='command', required=True)

        # Add command
        parser_add = subparsers.add_parser('add', help='Add a new task')
        parser_add.add_argument('description', type=str, help='Description of the task')
        parser_add.add_argument('--priority', type=int, help='Optional priority level (integer)')
        parser_add.add_argument('--due', type=str, help='Optional due date (YYYY-MM-DD)')

        # List command
        parser_list = subparsers.add_parser('list', help='List tasks')
        parser_list.add_argument('--status', choices=['all', 'pending', 'done'], default='all', help='Filter tasks by status')

        # Done command
        parser_done = subparsers.add_parser('done', help='Mark a task as done')
        parser_done.add_argument('task_id', type=int, help='ID of the task to mark done')

        # Delete command
        parser_delete = subparsers.add_parser('delete', help='Delete a task')
        parser_delete.add_argument('task_id', type=int, help='ID of the task to delete')

    def parse_and_execute(self, args=None):
        args = self.parser.parse_args(args)

        if args.command == 'add':
            task = self.task_manager.add_task(args.description, args.priority, args.due)
            print(f"Task added with ID {task.id}: {task.description}")

        elif args.command == 'list':
            tasks = self.task_manager.list_tasks(args.status)
            if not tasks:
                print("No tasks found.")
                return
            for task in tasks:
                status_symbol = '[x]' if task.status == 'done' else '[ ]'
                priority_str = f" (Priority {task.priority})" if task.priority is not None else ''
                due_str = f" (Due {task.due_date})" if task.due_date else ''
                print(f"{task.id}. {status_symbol} {task.description}{priority_str}{due_str}")

        elif args.command == 'done':
            success = self.task_manager.mark_done(args.task_id)
            if success:
                print(f"Task {args.task_id} marked as done.")
            else:
                print(f"Task {args.task_id} not found or already done.")

        elif args.command == 'delete':
            success = self.task_manager.delete_task(args.task_id)
            if success:
                print(f"Task {args.task_id} deleted.")
            else:
                print(f"Task {args.task_id} not found.")
