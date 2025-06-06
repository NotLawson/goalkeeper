# Main Server File
print("Welcome to JCI!")

# There are a couple of modules and libraries that are used by the application, like the auth module and the database module.
# We must initalize them here, and in a specific order due to dependencies.
# The order is as follows:
# 0. Base libraries
# 1. Config module
# 2. Logging
# 3. Database module
# 4. Auth module
# 5. File manager module
# 6. Flask
# 7. Core
# 8. Applets

# 0. Base libraries
import os, sys, time, json, datetime, re, random, string, base64, hashlib, binascii, uuid

# 1. Config module
print("Loading config...")
from modules.config import Config
config = Config('config.json')
print("Config loaded!")

# 2. Logging
import logging as log
if config.get("logging", "info") == "debug":
    level = log.DEBUG
elif config.get("logging", "info") == "info":
    level = log.INFO
elif config.get("logging", "info") == "warning":
    level = log.WARNING
elif config.get("logging", "info") == "error":
    level = log.ERROR
elif config.get("logging", "info") == "critical":
    level = log.CRITICAL
else:
    level = log.INFO

print("Setting up logging...")
import logging as log
log.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')
log.info("Logging initialized")

# 3. Database module
log.info("Loading database module...")
from modules.database import Database
database = Database(
    host=config.get("database", {}).get("host", "localhost"),
    port=config.get("database", {}).get("port", 5432),
    user=config.get("database", {}).get("user", "postgres"),
    password=config.get("database", {}).get("password", "password"),
    dbname=config.get("database", {}).get("database", "jci"),
)
log.info("Database module loaded!")

# 4. Auth module
log.info("Loading auth module...")
from modules.auth import Authentication
auth = Authentication(database)
log.info("Auth module loaded!")

# 5. File manager module
# Not created yet.

# 6. Flask
log.info("Setting up Flask...")
from flask import Flask, request, jsonify, render_template, redirect, send_file, make_response
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get("secret_key")
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB limit for uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'} # limit file types to images only
log.info("Flask setup complete!")

# 7. Core
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
        app.add_url_rule("/applet"+url, view_func=lambda **kwargs: self.render(function(**kwargs)), methods=methods)
    
    def render(self, response):
        """
        Render the response with the applet data.
        :param response: The response to render. Should be the result of a render_template call, or a string containing HTML.
        :return: The rendered response.
        """
        head, body = self.separate_head_body(response)

        # Get user
        user = auth.auth(request)

        # Render the response with the applet data
        return render_template("render.html", content=body, head=head, user=user)   

    def separate_head_body(html_string):
        """
        Separates the head and body sections from an HTML string.
        """
        head_match = re.search(r"<head>(.*?)</head>", html_string, re.IGNORECASE | re.DOTALL)
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html_string, re.IGNORECASE | re.DOTALL)

        head_content = head_match.group(1).strip() if head_match else None
        body_content = body_match.group(1).strip() if body_match else None

        return head_content, body_content
    
core = Core(app, [])
    
# 8. Applets
from applets import * # import all applets

app.run(host="0.0.0.0", port=int(config.get("port", 8080)), debug=False)