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

# 0. Base libraries
import os, sys, time, json, datetime, re, random, string, base64, hashlib, binascii, uuid
import requests, importlib

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

@app.context_processor
def inject_global_variables():
    return dict(
        datetime=datetime,
        int=int,
        str=str,
        len=len,
        enumerate=enumerate,
        round=round
    )

## Website Structure
# Accounts
#  - Login (/accounts/login)
#  - Register (/accounts/register)
#  - Logout (/accounts/logout)
#  - My Account (/accounts/me)
# My
#  - Dashboard (/my/dashboard)
#  - Profile (/my/profile)
#  - Goals (/my/goals)
#  - Tasks (/my/tasks)
#  - Create Goal (/my/goals/create)
#  - Edit Goal (/my/goals/edit/<goal_id>)
# Misc
#  - Index (/)
#  - About (/about)
# Admin
#  - Dashboard (/admin/dashboard)
#  - Users (/admin/users)
#  - Goals (/admin/goals)
#  - Tasks (/admin/tasks)

# Accounts

# Login (/accounts/login)
@app.route('/account/logins/', methods=['GET', 'POST'])
def login():
    if auth(request)[0]:
        return redirect(request.args.get('next', '/my/dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        success, token = auth.login(username, password)
        if success:
            resp = make_response(redirect(request.args.get('next', '/my/dashboard')))
            resp.set_cookie('token', token)
            return resp
        else:
            return render_template('accounts_login.html', error=token)

    return render_template('accounts_login.html')

# Register (/accounts/register)
@app.route('/accounts/register', methods=['GET', 'POST'])
def register():
    if auth(request)[0]:
        return redirect('/my/dashboard')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('name')
        success, msg = auth.register_user(username, password, email, name)
        if success:
            _, token = auth.login(username, password)
            resp = make_response(redirect('/my/dashboard'))
            resp.set_cookie('token', token)
            return resp
        else:
            return render_template('register.html', error=msg)

    return render_template('accounts_register.html')

# Logout (/accounts/logout)
@app.route('/accounts/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('token', '', expires=0)
    return resp

# My Account (/accounts/me)
@app.route('/accounts/me')
def my_account():
    return render_template('misc_notbuilt.html')

# My
# Dashboard (/my/dashboard)
@app.route('/my/dashboard')
def my_dashboard():
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    return render_template('misc_notbuilt.html')

# Profile (/my/profile)
@app.route('/my/profile')
def my_profile():
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    return render_template('misc_notbuilt.html')

# Goals (/my/goals)
@app.route('/my/goals')
def my_goals():
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    return render_template('misc_notbuilt.html')

# Tasks (/my/tasks)
@app.route('/my/tasks')
def my_tasks():
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    return render_template('misc_notbuilt.html')

# Create Goal (/my/goals/create)
@app.route('/my/goals/create')
def my_goals_create():
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    return render_template('misc_notbuilt.html')

# Edit Goal (/my/goals/edit/<goal_id>)
@app.route('/my/goals/edit/<goal_id>')
def my_goals_edit(goal_id):
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    return render_template('misc_notbuilt.html')

# Misc
# Index (/)
@app.route('/')
def index():
    if auth(request)[0]:
        return redirect('/my/dashboard')
    return render_template('misc_index.html')

# About (/about)
@app.route('/about')
def about():
    return render_template('misc_about.html')

# Admin
# Dashboard (/admin/dashboard)
@app.route('/admin/dashboard')
def admin_dashboard():
    a, user = auth(request)
    if not a or 'admin' not in user[10]:
        return redirect('/accounts/login?next=' + request.path)
    
    return render_template('misc_notbuilt.html')

# Users (/admin/users)
@app.route('/admin/users')
def admin_users():
    a, user = auth(request)
    if not a or 'admin' not in user[10]:
        return redirect('/accounts/login?next=' + request.path)
    
    return render_template('misc_notbuilt.html')

# Goals (/admin/goals)
@app.route('/admin/goals')
def admin_goals():
    a, user = auth(request)
    if not a or 'admin' not in user[10]:
        return redirect('/accounts/login?next=' + request.path)
    
    return render_template('misc_notbuilt.html')

# Tasks (/admin/tasks)
@app.route('/admin/tasks')
def admin_tasks():
    a, user = auth(request)
    if not a or 'admin' not in user[10]:
        return redirect('/accounts/login?next=' + request.path)
    
    return render_template('misc_notbuilt.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config.get("port", 8080)), debug=False)