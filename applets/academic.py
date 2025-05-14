# Academic Applet

# Main Config
name = "Academic Wellbeing"
base = "academic"


# Applet
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from __main__ import core

app = Blueprint(name, __name__, template_folder='templates', static_folder='static')
