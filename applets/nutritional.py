# Nutritional Applet
# flask is pretty important for a flask applet
from __main__ import core

# applet function
def nut_main():
    return 'it works kinda'

core.register_page(mental_main, '/nutritional')