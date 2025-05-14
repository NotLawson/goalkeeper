# Main Server File
import os, sys, time, json, datetime
from flask import Flask, request, jsonify, render_template, redirect, send_file, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

# Each section is split into its own file for better organization
# The only section that is not split is the main server file, as it is the core section (JCI Core).
# Import other sections
#from applets import *

# Core
# JCI Core contains the base level stuff for the application. Accounts, notifications, goals, etc.
# It also handles managing the applets, hence being on a different level to them.
# How this works is that when someone requests and applet, it will contsruct the data, get a request ready, but then send it to core to be packaged into the app. 
# This allows the applets to work independently from each other whilst still including sidebars, notification, and other HUD elements.
# The logic for this is contained in this file, as the function below.
# This class is used by the main server, and then the resulting object is imported by the applets via __main__
class Core:
    def __init__(self, applets: list):
        self.applets = applets # List containing the applet objects. This is used to get names, url bases etc.
    
    def render(self, response, json=False):
        return render_template('display.html', response=response, json=json)
@app.route('/')
def index():
    """
    Main page of the application.
    :return: Rendered template of the main page.
    """
    resp = render_template('index.html')
    core = Core(applets = [])
    return core.render(resp)

app.run(port=5000, debug=True)