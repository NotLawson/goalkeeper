# Academic Applet

# Main Config
name = "Academic Wellbeing"
base = "academic"


# Applet
from flask import render_template, abort

from __main__ import app, database, core, log
log.info("Academic Wellbeing applet loading...")

def index():
    """
    Index page for the Academic Wellbeing applet.
    """
    # Get the user id from the session
    user_id = core.get_user_id()
    if not user_id:
        return abort(401)

    # Get the user data from the database
    user_data = db.get_user_data(user_id)
    if not user_data:
        return abort(404)

    # Render the index page
    return render_template("academic/index.html", user_data=user_data)

core.register_page(index, "/academic", methods=["GET"])


log.info("Academic Wellbeing applet loaded!")