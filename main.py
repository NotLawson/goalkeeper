# Main Server File
import os, sys, time, json, datetime, re
from flask import Flask, request, jsonify, render_template, redirect, send_file, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

# Each section is split into its own file for better organization
# The only section that is not split is the main server file, as it is the core section (JCI Core).
app.register_blueprint()

# Core
# JCI Core contains the base level stuff for the application. Accounts, notifications, goals, etc.
# It also handles managing the applets, hence being on a different level to them.
# How this works is that when someone requests and applet, it will contsruct the data, get a request ready, but then send it to core to be packaged into the app. 
# This allows the applets to work independently from each other whilst still including sidebars, notification, and other HUD elements.
# The logic for this is contained in this file, as the function below.
# This class is used by the main server, and then the resulting object is imported by the applets via __main__
class Core:
    def __init__(self, app, applets: list):
        self.app = app
        self.applets = applets # List containing the applet objects. This is used to get names, url bases etc.
    
    def register_page(self, function, url, methods=["GET"]):
        """
        Register a page with the applet.
        :param function: The function to call when the page is requested.
        :param url: The URL to register the page at.
        :param methods: The HTTP methods to allow for this page.
        """
        app.add_url_rule(url, view_func=lambda: self.render(function), methods=methods)
    
    def render(self, response):
        """
        Render the response with the applet data.
        :param response: The response to render. Should be the result of a render_template call, or a string containing HTML.
        :return: The rendered response.
        """
        head, body = self.separate_head_body(response)

        # Get user
        auth

        # Render the response with the applet data
        return render_template("applet.html", content=body, head=head)   

    def separate_head_body(html_string):
        """
        Separates the head and body sections from an HTML string.
        """
        head_match = re.search(r"<head>(.*?)</head>", html_string, re.IGNORECASE | re.DOTALL)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html_string, re.IGNORECASE | re.DOTALL)

        head_content = head_match.group(1).strip() if head_match else None
        body_content = body_match.group(1).strip() if body_match else None

        return head_content, body_content

    


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