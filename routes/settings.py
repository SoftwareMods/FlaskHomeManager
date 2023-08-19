"""Routes for tools"""
import json
import os
from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    session,
    Response,
)  # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import render_template, loadJSONFromFile, saveJSONToFile, getNewId
from helpers.settings import settings_file, system_settings
from helpers.chores import diffs_file

settings = Blueprint("settings", __name__)


@settings.route("/settings", methods=["GET", "POST"])
def index():
    """ "Settings page"""

    if request.method == "POST":
        settings_dict = loadJSONFromFile(settings_file)

        # Get each setting from the submission
        currency = request.form.get("currency")

        # Update the dictionary
        settings_dict["currency"] = currency
        for key in request.form.keys():
             settings_dict[key] = request.form.get(key)

        # Save the settings
        if saveJSONToFile(settings_file, settings_dict):
            flash(f"Successfully updated settings", "success")
        else:
            flash(f"Failed to update settings", "error")

    return render_template(
        "settings/index.html",
        system_settings=loadJSONFromFile(settings_file),
        diffs=loadJSONFromFile(diffs_file),
        sidebar=True,
        tables=True,
    )
