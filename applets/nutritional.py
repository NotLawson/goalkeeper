# Nutritional Applet
# flask is pretty important for a flask applet
from __main__ import core
from flask import render_template

# applet function
def nut_main():
    return render_template("nutritional.html", title="Nutritional Wellbeing", description="A space to focus on nutritional health and wellbeing.")

core.register_page(nut_main, '/nutritional')