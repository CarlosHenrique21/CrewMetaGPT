# cli.py

import argparse
from task_manager import TaskManager

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='CLI Task Manager')
    parser.add_argument('command', choices=['add', 'list', 'done', 'delete'], help='Command to execute')
    parser.add_argument('--title', type=str, help='Title of the task')
    parser.add_argument('--description', type=str, help='Description of the task')
    parser.add_argument('--id', type=int, help='ID of the task to mark as done or delete')

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the Task Manager
    task_manager = TaskManager()

    # Execute commands based on user input
    if args.command == 'add':
        if not args.title:
            print("Error: Title is required to add a task.")
            return
        task_manager.add_task(args.title, args.description)
        print("Task added successfully.")

    elif args.command == 'list':
        tasks = task_manager.list_tasks()
        for task in tasks:
            print(task)

    elif args.command == 'done':
        if args.id is None:
            print("Error: Task ID is required to mark as done.")
            return
        task_manager.mark_done(args.id)
        print("Task marked as done.")

    elif args.command == 'delete':
        if args.id is None:
            print("Error: Task ID is required to delete a task.")
            return
        task_manager.delete_task(args.id)
        print("Task deleted successfully.")

if __name__ == '__main__':
    main()
