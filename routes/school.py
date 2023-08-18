"""Routes for tools"""
import json
import os
from flask import Blueprint, flash, request, session, Response # last one use for overriding and passing NAVIGATION to all templates
from markupsafe import escape
from helpers.common import render_template

school = Blueprint('school', __name__)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@school.route('/school')
def index():
    """"default landing page"""

    return render_template('school/index.html', sidebar=True)