# Academic Applet

# Main Config
name = "Academic Wellbeing"
base = "academic"


# Applet
from flask import render_template, abort
import datetime, random

from __main__ import app, database, core, log
log.info("Academic Wellbeing applet loading...")

def index(path):
    """
    Index page for the Academic Wellbeing applet.
    """
    # Render the index page
    return render_template("academic.html", time=datetime.datetime.now().strftime("%H:%M:%S"), random_number=random.randint(1, 100), path=path)

core.register_page(index, "/academic", methods=["GET"])


log.info("Academic Wellbeing applet loaded!")