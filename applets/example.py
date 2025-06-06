# Example applet
from flask import render_template
from __main__ import core, database, log

name = "Example Applet"
base = "/example"


# Main Page
def index():
    """
    Index page as an example.
    """
    return render_template("example/index.html")