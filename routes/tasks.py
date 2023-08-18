"""Routes for tools"""
import json
import os
from flask import Blueprint, flash, request, session, Response # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import redirect, render_template, saveJSONToFile, loadJSONFromFile, getNewId
from helpers.tasks import task_file

tasks = Blueprint('tasks', __name__)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@tasks.route('/tasks', methods=['GET','POST'])
def index():
    """"default landing page"""

    update_task = False
    mytasks = loadJSONFromFile(task_file)

    if request.method == 'POST':

        if request.form.get('UpdateTask'):
            task_id = int(request.form.get('task_id'))
        else:
            task_id = getNewId(mytasks)

        task_name = request.form.get('new-task')
        task_due  = request.form.get('task-due')
        task_complete  = 1 if request.form.get('task-complete') == 'on' else 0
        json_obj = {"id": task_id, "task_name": task_name, "task_due": task_due, "complete": task_complete}
        if request.form.get('UpdateTask'):
            for i in range(len(mytasks)):
                if mytasks[i]['id'] == task_id:
                    mytasks[i]['name'] = task_name
                    mytasks[i]['task_due'] = task_due
                    mytasks[i]['complete'] = task_complete
                    break
        else:
            mytasks.append(json_obj)
        saveJSONToFile(task_file, mytasks)
    elif request.method == 'GET':
        if request.args.get('update') != None:
            update_id = int(request.args.get('update'))
            for i in range(len(mytasks)):
                if mytasks[i]['id'] == update_id:
                    update_task = mytasks[i]

    return render_template('tasks/index.html', sidebar=True, tables=True, tasks=mytasks, update_task=update_task)

@tasks.route('/tasks/delete/<int:task_id>', methods=['GET','POST'])
def delete_task(task_id):
    """"delete given task"""

    deleted = False
    mytasks = loadJSONFromFile(task_file)
    for i in range(len(mytasks)):
        if mytasks[i]['id'] == task_id:
            del mytasks[i]
            saveJSONToFile(task_file, mytasks)
            deleted = True
            break

    if deleted:
        flash('Successfully deleted task', 'success')
    else:
        flash('Failed to delete task', 'error')

    return redirect(f'/tasks')

@tasks.route('/tasks/complete/<int:task_id>', methods=['GET','POST'])
def complete_task(task_id):
    """"complete given task"""

    completed = False
    mytasks = loadJSONFromFile(task_file)
    for i in range(len(mytasks)):
        if mytasks[i]['id'] == task_id:
            mytasks[i]['complete'] = 1
            saveJSONToFile(task_file, mytasks)
            completed = True
            break

    if completed:
        flash('Successfully marked task as complete', 'success')
    else:
        flash('Failed to mark task as complete', 'error')

    return redirect(f'/tasks')

@tasks.route('/tasks/incomplete/<int:task_id>', methods=['GET','POST'])
def incomplete_task(task_id):
    """"incomplete given task"""

    incompleted = False
    mytasks = loadJSONFromFile(task_file)
    for i in range(len(mytasks)):
        if mytasks[i]['id'] == task_id:
            mytasks[i]['complete'] = 0
            saveJSONToFile(task_file, mytasks)
            incompleted = True
            break

    if incompleted:
        flash('Successfully marked task as incomplete', 'success')
    else:
        flash('Failed to mark task as incomplete', 'error')

    return redirect(f'/tasks')
