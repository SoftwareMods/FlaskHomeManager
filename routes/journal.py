"""Routes for tools"""
import json
import os
from flask import Blueprint, Markup, flash, request, session, Response # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import redirect, render_template, saveJSONToFile, loadJSONFromFile, getNewId
from helpers.journal import journal_file

journal = Blueprint('journal', __name__)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@journal.route('/journal', methods=['GET','POST'])
def index():
    """"default landing page"""

    entries = loadJSONFromFile(journal_file)
    
    data=False
    if request.method == "GET":
        if request.args.get('update') != None:
            entry_id = int(request.args.get('update'))
            print(f"Get ID {entry_id}")
            for i in range(len(entries)):
                if entries[i]['id'] == entry_id:
                    data = entries[i]
                    break
    elif request.method == "POST":
        if request.form.get('UpdateEntry'):
            entry_id = int(request.form.get('id'))
        else:
            entry_id = getNewId(entries)
        entry = request.form.get('journal-entry')
        datetime = request.form.get('journal-date')
        title = request.form.get('journal-title')
        data = { 'id': entry_id, 'datetime': datetime, 'title': title, 'entry': entry }
        # if an update
        if request.form.get('UpdateEntry'):
            for i in range(len(entries)):
                if entries[i]['id'] == entry_id:
                    entries[i]['title'] = title
                    entries[i]['datetime'] = datetime
                    entries[i]['entry'] = entry
                    break
        # new entry
        else:
            entries.append(data)
        saveJSONToFile(journal_file, entries)

    return render_template('journal/index.html', sidebar=True, editor=True, data=data)

@journal.route('/journal/list')
def entry_list():
    """"Datatable of entries"""

    entries = loadJSONFromFile(journal_file)
    for i in range(len(entries)):
        entries[i]['entry'] = Markup(entries[i]['entry'])   
    
    return render_template('journal/list.html', sidebar=True, tables=True, entries=entries)

@journal.route('/journal/delete/<int:entry_id>', methods=['GET','POST'])
def delete_entry(entry_id):
    """"delete given journal entry"""

    deleted = False
    entries = loadJSONFromFile(journal_file)
    for i in range(len(entries)):
        if entries[i]['id'] == entry_id:
            del entries[i]
            saveJSONToFile(journal_file, entries)
            deleted = True
            break

    if deleted:
        flash('Successfully deleted entry', 'success')
    else:
        flash('Failed to delete entry', 'error')

    return redirect(f'/journal/list')