# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    request,
    session,
    url_for,
    render_template as real_render_template,
    Response,
)  # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import render_template, loadJSONFromFile
from helpers.tasks import task_file
from helpers.bills import bill_file
from helpers.chores import *
from helpers.shopping import shopping_file
from nav import NAVIGATION

frontend = Blueprint("frontend", __name__)


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route("/")
def index():
    """ "default landing page"""

    tasks = loadJSONFromFile(task_file)
    bills = loadJSONFromFile(bill_file)
    chores = getDueChores()
    floors = loadJSONFromFile(floors_file)
    locations = loadJSONFromFile(locations_file)
    assignees = loadJSONFromFile(assignee_file)
    shopping_list = loadJSONFromFile(shopping_file)

    return render_template(
        "index.html",
        floors=floors,
        locations=locations,
        assignees=assignees,
        tables=True,
        chores=chores,
        tasks=tasks,
        bills=bills,
        shopping=shopping_list
    )


@frontend.route("/icons")
def icons():
    file1 = open("static/fontawesomefree/css/all.css", "r")
    Lines = file1.readlines()
    iconlist = [
        l.split("::")[0].split(":")[0].split(".")[1] for l in Lines if "before" in l
    ]

    return render_template("icons.html", tables=True, icons=iconlist)
