import argparse
from tasks import add_task, list_tasks, complete_task, delete_task, search_tasks


def main():
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")

    # list
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Show completed tasks too")

    # complete
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")

    # delete
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID")

    # search
    search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
    search_parser.add_argument("query", help="Keyword to search")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks(show_all=args.all)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "search":
        search_tasks(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
