#!/bin/python3

commands = {}
def clicommand(command):
    commands[command.__name__] = command

def dump_tasks():
    with open(TASK_FILE, 'w') as task_file:
         json.dump(tasks, task_file)

class BasicError(Exception):
        def __init__(self, message="Usage Error.", value=None):
            self.message = message
            self.value = value
            super().__init__(self.message)

@clicommand
def add(*args):
    if len(args) != 1:
        raise BasicError("Bad argument count")
    description = args[0]
    task_id = tasks['task_count']
    task_id += 1
    tasks['task_count'] = task_id
    date_created = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    tasks[task_id] = { 'id' : task_id,
                      'description': description,
                      'status' : 'todo',
                      'created_at' : date_created,
                      'updated_at' : date_created
                      }
    
    dump_tasks()
    print(f"Added task with ID: {task_id}")

@clicommand
def update(*args):
    if len(args) != 2:
        raise BasicError("Bad argument count")
    if args[0] not in tasks:
        raise BasicError("Task with that id does not exist")
    tasks[args[0]]['description'] = args[1]
    tasks[args[0]]['updated_at'] = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    dump_tasks()
    print(f"Upated task with ID {args[0]} with {args[1]}")

@clicommand
def delete(*args):
    if len(args) != 1:
        raise BasicError("Bad argmument count")
    elif args[0] not in tasks:
        raise Exception("Task with that ID does to exist")
    del tasks[args[0]]
    dump_tasks()
    print(f"Deleted task with ID: {args[0]}")

@clicommand
def mark(*args):
    if len(args) != 2:
        raise BasicError("Bad argmuent count")
    elif args[0] not in MARK_OPTIONS:
        raise BasicError("Bad Mark option")
    elif args[1] not in tasks:
        raise BasicError("No task with that ID")
    tasks[args[1]]['status'] = args[0]
    tasks[args[1]]['updated_at'] = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    dump_tasks()
    print(f"Task with ID: {args[1]} marked as {args[0]}")

@clicommand
def list(*args):
    if len(args) not in (0,1):
        raise BasicError("Bad argmuent count")

    if len(args) == 1 and args[0] not in MARK_OPTIONS:
        raise BasicError("Bad status option")

    del tasks['task_count']
    todo_count = sum([1 for idx, task in tasks.items() if task['status'] == 'todo'])
    done_count = sum([1 for idx, task in tasks.items() if task['status'] == 'done'])
    in_progress_count = sum([1 for idx, task in tasks.items() if task['status'] == 'in-progress'])



    print(BANNER)
    print(f"Task count: {len(tasks)} todo: {todo_count} done: {done_count} in-progress: {in_progress_count}\n")
    print(f"{'DATE':20} {'STATUS':12} {'ID':<3} {'DESCRIPTION'}")
    for idt, task in tasks.items():
        if len(args) == 0 or task['status'] == args[0]:
            print(f"{task['updated_at']:20} {task['status']:12} {task['id']:<3} {task['description']}")



if __name__ == '__main__':
    import sys
    import json
    from datetime import datetime
    TASK_FILE = 'task-cli-tasks.json'
    MARK_OPTIONS = ('todo', 'done', 'in-progress')
    help_string = \
"""
Usage: task-cli.py command [options]
commands: add, update, delete, list, mark
add:
    Add a new task
    options:
    no options, just enter description
    eg. task-cli.py add "Go shopping"
upadte:
    Upadate the description of an existing task
    options:
    id of task to update
    eg. task-cli.py update 1 "Prepare dinner"
delete:
    Delete a task
    options:
    id of task to delete
    eg. task-cli.py delete 1
list:
    List tasks
    options:
    no options will list all tasks
    eg. task-cli.py list
    status of tasks to display. (status are todo, in-progress, done)
    eg. task-cli.py list done
mark:
    Mark a task with a status
    options:
    id of the task to mark and status to mark as (status are todo, in-progress, done)
    eg. task-cli.py mark done 1

"""
    BANNER = \
"""
====================================================
                TASK CLI
by: albertbagyo              github.com/albertbagyo
====================================================
"""
    try:
        with open(TASK_FILE, 'r') as tasks_file:
            tasks = json.load(tasks_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e :
            tasks = {'task_count' : 0} 

    try:
        command = commands[sys.argv[1]]
        command(*sys.argv[2:]) 
    except BasicError as e:
        print(e)
    except Exception as e:
        print(help_string)
        #print(e)
