# Mental Applet

# flask is pretty important for a flask applet
from __main__ import core
from flask import render_template

# applet function
def mental_main():
    return render_template("mental.html", title="Mental Wellbeing", description="A space to focus on mental health and wellbeing.")

core.register_page(mental_main, '/mental')