#!/bin/python3

commands = {}
def clicommand(command):
    commands[command.__name__] = command

@clicommand
def add(*args):
    if len(args) != 1:
        raise Exception("Too many arguments")
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
    with open(TASK_FILE, 'w') as task_file:
        json.dump(tasks, task_file)

@clicommand
def update(*args):
    pass

@clicommand
def delete():
    pass

@clicommand
def mark():
    pass

@clicommand
def list(*args):

    print(f"Task count: {tasks['task_count']}\n")
    for idt, task in tasks.items():
        if isinstance(task,int):
            continue
        if len(args) == 0 or task['status'] == args[0]:
            print(f"{task['created_at']} {task['status']} {task['id']} {task['description']}\n")



if __name__ == '__main__':
    import sys
    import json
    from datetime import datetime
    TASK_FILE = 'task-cli-tasks.json'
    help_string = \
"""
    Something went wrong!
    commands = {
            'add': _add,
            'delete': _delete,
            'update': _update,
            'mark': _mark,
            'list': _list
            }
"""
    try:
        with open(TASK_FILE, 'r') as tasks_file:
            tasks = json.load(tasks_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e :
            tasks = {'task_count' : 0} 

    try:
        command = commands[sys.argv[1]]
        command(*sys.argv[2:]) 
    except:
        print(e)
        print(help_string)
        exit()
