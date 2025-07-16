# Physical Applet
# flask is pretty important for a flask applet
from flask import render_template
from __main__ import core

# applet function
def physical_main():
    return render_template('physical.html')

core.register_page(physical_main, '/physical')