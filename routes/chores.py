"""Routes for tools"""
import json
import os
from flask import (
    Blueprint,
    flash,
    request,
    session,
    Response,
)  # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import render_template, redirect, saveJSONToFile, getNewId
from helpers.chores import *
from datetime import date

chores = Blueprint("chores", __name__)
today = date.today()
today_str = today.strftime("%m/%d/%Y")


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@chores.route("/chores", methods=["GET", "POST"])
def index():
    """ "default landing page"""

    chores = getDueChores()
    assignees = getAssignees()
    floors = loadJSONFromFile(floors_file)
    freqs = loadJSONFromFile(freqs_file)
    locations = loadJSONFromFile(locations_file)

    return render_template(
        "chores/index.html",
        floors=floors,
        tables=True,
        freqs=freqs,
        locations=locations,
        chores=chores,
        assignees=assignees,
        sidebar=True,
    )


@chores.route("/chores-add", methods=["GET", "POST"])
def add_chore():
    """ "Page for adding a new chore"""
    chores = getChores()
    assignees = getAssignees()
    diffs = loadJSONFromFile(diffs_file)
    freqs = loadJSONFromFile(freqs_file)
    floors = loadJSONFromFile(floors_file)
    locations = loadJSONFromFile(locations_file)
    update = False

    if request.method == "POST":
        # request.form
        # ImmutableMultiDict([('name', 'adsf'), ('floor', '1'), ('location', '1'), ('default-assignee', '3'), ('difficulty', '3'), ('freq', '2')])
        if not request.form.get("update_id"):
            new_chore = {
                "id": getNewId(chores),
                "name": request.form.get("name"),
                "floor": int(request.form.get("floor")),
                "location": int(request.form.get("location")),
                "default_assignee": int(request.form.get("default-assignee")),
                "freq": int(request.form.get("freq")),
                "difficulty": int(request.form.get("difficulty")),
                "last_completed_date": "",
                "last_completed_by": None,
                "completed_dates": []
            }
            chores.append(new_chore)
        else:
            chore_id = int(request.form.get("update_id"))
            for i in range(len(chores)):
                if chores[i]["id"] == chore_id:
                    chores[i]["name"] = request.form.get("name")
                    chores[i]["floor"] = int(request.form.get("floor"))
                    chores[i]["location"] = int(request.form.get("location"))
                    chores[i]["default_assignee"] = int(
                        request.form.get("default-assignee")
                    )
                    chores[i]["freq"] = int(request.form.get("freq"))
                    chores[i]["difficulty"] = int(request.form.get("difficulty"))
                    break

        if saveJSONToFile(chore_file, chores):
            flash("Successfully saved chore", "info")
        else:
            flash("Failed to save chore", "error")

    elif request.method == "GET":
        if request.args.get("update"):
            update_id = int(request.args.get("update"))
            for i in range(len(chores)):
                if chores[i]["id"] == update_id:
                    update = chores[i]
                    break

    return render_template(
        "chores/add_chore.html",
        floors=floors,
        locations=locations,
        freqs=freqs,
        diffs=diffs,
        update=update,
        assignees=assignees,
        tables=True,
        chores=chores,
        sidebar=True,
    )


@chores.route("/chores/complete/", methods=["GET", "POST"])
def complete_chore():
    """Process for completing chore"""
    chores = getChores()
    assignees = getAssignees()

    if request.method == "POST":
        by_id = int(request.form.get("default-assignee"))
        chore_id = int(request.form.get("chore_id"))
        # Find the chore and update
        # last_completed_by
        # last_completed_date
        # completed_dates
        difficulty = 0
        for i in range(len(chores)):
            if chores[i]["id"] == chore_id:
                chores[i]["last_completed_date"] = today_str
                chores[i]["last_completed_by"] = by_id
                chores[i]["completed_dates"].append({"date": today_str, "by": by_id})
                difficulty = chores[i]["difficulty"]
                chore_name = chores[i]["name"]
                to_bank = difficulty * 0.25
                break
        if saveJSONToFile(chore_file, chores):
            flash(f"Successfully marked {chore_name} as completed", "success")
            # Task officially completed, payout to assignee
            for i in range(len(assignees)):
                if assignees[i]["id"] == by_id:
                    assignees[i]["bank"] += to_bank
                    assignee_name = assignees[i]["name"]
                    assignee_bank = assignees[i]["bank"]
                    break
            if saveJSONToFile(assignee_file, assignees):
                flash(f"Updated {assignee_name} bank to {assignee_bank}", "success")
            else:
                flash(
                    f"Failed to update {assignee_name} bank to {assignee_bank}",
                    "success",
                )
        else:
            flash(
                f"Failed to mark {chores[chore_id]} as completed by {assignees[by_id]}",
                "error",
            )

    return redirect(f"/chores")


@chores.route("/chores-assignees", methods=["GET", "POST"])
def assignees():
    """ "Add and list assignees for chores"""
    assignees = getAssignees()
    update = False
    if request.method == "POST":
        if request.form.get("name") and request.form.get("bedtime"):
            name = request.form.get("name")
            bedtime = request.form.get("bedtime")
            bank = request.form.get("bank")
            if not request.form.get("update_id"):
                new_assignee = {
                    "id": getNewId(assignees),
                    "name": name,
                    "bedtime": int(bedtime),
                    "bank": float(bank),
                }
                assignees.append(new_assignee)
            else:
                update_id = int(request.form.get("update_id"))
                for i in range(len(assignees)):
                    if assignees[i]["id"] == update_id:
                        assignees[i]["name"] = name
                        assignees[i]["bedtime"] = bedtime
                        assignees[i]["bank"] = float(bank)
                        break
            if saveJSONToFile(assignee_file, assignees):
                flash("Successfully saved assignee", "success")
            else:
                flash("Failed to save assignee", "error")
    elif request.method == "GET":
        if request.args.get("update"):
            update = request.args.get("update")

    return render_template(
        "chores/assignees.html", update=update, assignees=assignees, sidebar=True
    )


@chores.route("/chores/delete-assignee/<int:id>", methods=["GET", "POST"])
def delete_assignee(id):
    """ "delete given assignee"""

    assignees = getAssignees()
    for i in range(len(assignees)):
        if assignees[i]["id"] == id:
            del assignees[i]
            break

    if saveJSONToFile(assignee_file, assignees):
        flash("Successfully deleted assignee", "success")
    else:
        flash("Failed to delete assignee", "error")

    return redirect(f"/chores-assignees")


@chores.route("/chores/delete-chore/<int:id>", methods=["GET", "POST"])
def delete_chore(id):
    """Delete given chore"""

    return redirect(f"/chores-add")
