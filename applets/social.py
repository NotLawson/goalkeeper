#social
from flask import render_template
from __main__ import core

# applet function
def physical_main():
    return render_template('social.html')

core.register_page(physical_main, '/social')