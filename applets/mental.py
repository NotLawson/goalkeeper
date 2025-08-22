# Mental applet
from flask import render_template
#from __main__ import database, log

## Pages
# Main Page
def index(user):
    """
    Index page as an example.
    """
    return render_template("mental.html")


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
        "name": "Mental Applet",
        "description": "This is the mental applet.",
        "url": "/mental"
    }
    