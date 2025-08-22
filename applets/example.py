# Example applet
from flask import render_template
#from __main__ import database, log

## Pages
# Main Page
def index(user):
    """
    Index page as an example.
    """
    return render_template("example/index.html")


# Init function
def init():
    """Initialize the applet."""

    return {
        "pages": [
            {
                "matcher": "/",
                "function": index,
                "methods": ["GET"]
            }
        ]
    }
## Info function
def info():
    """
    Example applet info.
    """
    return {
        "name": "Example Applet",
        "description": "This is an example applet.",
        "url": "/example"
    }
    