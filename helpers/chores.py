from helpers.common import saveJSONToFile, loadJSONFromFile
from datetime import date, datetime
from flask import flash as debug

today = date.today()
# today_str = today.strftime("%m/%d/%Y")
assignee_file = "data/chores/assignees.json"
chore_file = "data/chores/chores.json"
diffs_file = "data/chores/diff.json"
freqs_file = "data/chores/freq.json"
floors_file = "data/chores/floor.json"
locations_file = "data/chores/location.json"


def getAssignees():
    return loadJSONFromFile(assignee_file)


def saveAssignee(name, bedtime):
    assignees = getAssignees()
    assignees[name] = bedtime
    saveJSONToFile(assignee_file, assignees)
    return True


def getChores():
    return loadJSONFromFile(chore_file)


def saveChore(name, difficulty, freq):
    chores = getChores()
    chores[name] = (difficulty, freq)
    if not saveAllChores(chores):
        return False
    return True

def saveAllChores(chores):
    if not saveJSONToFile(chore_file, chores):
        return False
    return True

def getDueChores():
    # Get list of chores from chores.json
    chores = getChores()

    todo_list = []
    for chore in chores:
        # Check if due within frequency range
        freq  = chore['freq']
        freq_in_days = { 1: 1, 2: 14, 3: 30, 4: 365}
        last_completed = chore['last_completed_date']
        if last_completed:
            last_completed_obj = datetime.strptime(last_completed, "%m/%d/%Y").date()
            # compare the dates
            days_passed = (today - last_completed_obj).days
            if chore['name'] == "Pans":
                debug(f"days_passed: {days_passed}, freq_days: {freq_in_days[freq]}")
            if days_passed >= freq_in_days[freq]:
                todo_list.append(chore) 
        else:
            todo_list.append(chore)
        
    return todo_list