import sys
import argparse
from cli_task_manager.service import TaskManagerService

def main():
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('description', type=str, help='Description of the task')

    # List command
    subparsers.add_parser('list', help='List all tasks')

    # Done command
    parser_done = subparsers.add_parser('done', help='Mark task as done')
    parser_done.add_argument('task_id', type=int, help='ID of the task to mark done')

    # Delete command
    parser_delete = subparsers.add_parser('delete', help='Delete a task')
    parser_delete.add_argument('task_id', type=int, help='ID of the task to delete')

    args = parser.parse_args()

    service = TaskManagerService()

    try:
        if args.command == 'add':
            task_id = service.add_task(args.description)
            print(f"Task added with ID {task_id}")

        elif args.command == 'list':
            tasks = service.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print(f"{'ID':<5} {'Status':<8} {'Description'}")
                print('-' * 40)
                for task in tasks:
                    status = 'Done' if task.status == 'done' else 'Pending'
                    print(f"{task.id:<5} {status:<8} {task.description}")

        elif args.command == 'done':
            success = service.mark_done(args.task_id)
            if success:
                print(f"Task {args.task_id} marked as done.")
            else:
                print(f"Task {args.task_id} not found or already done.")

        elif args.command == 'delete':
            success = service.delete_task(args.task_id)
            if success:
                print(f"Task {args.task_id} deleted.")
            else:
                print(f"Task {args.task_id} not found.")

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        service.close()

if __name__ == '__main__':
    main()
