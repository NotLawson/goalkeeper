# Main Server File
print("GoalKeeper - Main server")

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
    password=config.get("database", {}).get("password", "postgres"),
    dbname=config.get("database", {}).get("database", "postgres"),
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
        round=round,
        ZeroDivisionError=ZeroDivisionError,
        load=json.loads,
        dump=json.dumps
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
#   - Goal Details (/my/goals/<goal_id>)
#  - Tasks (/my/tasks)
#   - Task Details (/my/tasks/<task_id>)
#  - Create Goal (/my/goals/create)
#  - Edit Goal (/my/goals/<goal_id>/edit)
#  - Notifications (/my/notifications)
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
@app.route('/accounts/login', methods=['GET', 'POST'])
def accounts_login():
    if auth(request)[0]: # check if the user is logged in
        return redirect(request.args.get('next', '/my/dashboard'))
    if request.method == 'POST':

        # get form data
        username = request.form.get('username')
        password = request.form.get('password')
        success, token = auth.login(username, password)

        # if login successful, set token and redirect to dashboard
        if success:
            resp = make_response(redirect(request.args.get('next', '/my/dashboard')))
            resp.set_cookie('token', token)
            return resp
        else:
            # if login failed, show error
            return render_template('accounts_login.html', error=token)

    # render the login page
    return render_template('accounts_login.html')

# Register (/accounts/register)
@app.route('/accounts/register', methods=['GET', 'POST'])
def accounts_register():
    if auth(request)[0]: # check if the user is logged in
        return redirect('/my/dashboard')

    if request.method == 'POST':

        # get form data
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        name = request.form.get('name')

        # attempt to register the user
        success, msg = auth.register_user(username, password, email, name)
        if success:
            # log the user in with new credentials, set token and redirect to the dashboard
            _, token = auth.login(username, password)
            resp = make_response(redirect('/my/dashboard'))
            resp.set_cookie('token', token)
            return resp
        else:
            # if registration failed, show error
            return render_template('accounts_register.html', error=msg)

    # render the registration page
    return render_template('accounts_register.html')

# Logout (/accounts/logout)
@app.route('/accounts/logout')
def accounts_logout():
    # logout endpoint used by the Logout button in the user settings screen

    # delete the user's token from the database. Since this endpoint is only accessible to logged in user, we can assume the token is present and valid
    success, msg = auth.delete_token(request.cookies.get('token'))
    if success:
        # clear the token from the client and redirect to the homepage
        resp = make_response(redirect('/'))
        resp.set_cookie('token', '', expires=0)
        return resp
    # if logout failed, show error in JSON format
    return jsonify({"error": msg}), 400

# My Account (/accounts/me)
@app.route('/accounts/me', methods=['GET', 'POST'])
def my_account():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    if request.method == 'POST': # if the user is updating their account

        # get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        tags = user[10] # keep existing tags

        # attempt to update the user
        success, msg = auth.update_user(auth(request)[1][0], username, password, email, name, tags)
        if success:
            # if update was successful, update user object returned with the new version and show success message
            _, user = auth(request)
            return render_template('accounts_me.html', complete=msg, user=user)
        else:
            # if update failed, show error
            return render_template('accounts_me.html', error=msg, user=user)
    
    # render the account page
    return render_template('accounts_me.html', user=user)


# My Dashboard (/my/dashboard)
@app.route('/my/dashboard')
def my_dashboard():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get the user's goals
    goals = database.execute_query("SELECT * FROM goals WHERE user_id = %s ORDER BY created_at ASC LIMIT 3;", (user[0],))

    tasks = []
    # for each goal, get the next 3 incomplete tasks
    for goal in goals:
        goal_tasks = database.execute_query("SELECT * FROM tasks WHERE goal_id = %s AND status = 'incomplete' ORDER BY created_at ASC LIMIT 3;", (goal[0],))
        tasks.extend(goal_tasks)
    
    # pass this information to jinja2 and render the dashboard
    return render_template('my_dashboard.html', user=user, goals=goals, tasks=tasks)

# Profile (/my/profile)
@app.route('/my/profile')
def my_profile():
    if not auth(request)[0]:
        return redirect('/accounts/login?next=' + request.path)
    
    # this page wasn't built due to the social features being cut
    # it's original purpose was to show a public profile for the user to others
    return render_template('misc_notbuilt.html')

# Goals (/my/goals)
@app.route('/my/goals')
def my_goals():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get the user's goals
    goals = database.execute_query("SELECT * FROM goals WHERE user_id = %s ORDER BY created_at DESC;", (user[0],))

    # render the goals page
    return render_template('my_goals.html', user=user, goals=goals)

# Goal Details (/my/goals/<goal_id>)
@app.route('/my/goals/<goal_id>')
def my_goals_goal(goal_id):
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get a specific goal and its tasks
    goal = database.execute_query("SELECT * FROM goals WHERE id = %s AND user_id = %s;", (goal_id, user[0]))

    # small bug with the database module. see the database module for more info
    goal = goal[0] if goal else False
    if not goal:
        # note: this page doesn't actually exist... sorry
        return render_template('misc_notfound.html'), 404
    
    # get the tasks for this goal
    tasks = database.execute_query("SELECT * FROM tasks WHERE goal_id = %s ORDER BY created_at DESC;", (goal[0],))

    # render the goal details page
    return render_template('my_goals_goal.html', user=user, goal=goal, tasks=tasks)

# Tasks (/my/tasks)
@app.route('/my/tasks')
def my_tasks():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get the user's goals
    goals = database.execute_query("SELECT * FROM goals WHERE user_id = %s ORDER BY created_at DESC;", (user[0],))
    tasks = []

    # unused logic here to filter tasks by status. it was determined that displaying all tasks was more useful
    # as a quick fix, i wrote this garbage. sorry

    #if request.args.get('filter', 'incomplete') == 'all':
    if True:
        for goal in goals:
            goal_tasks = database.execute_query("SELECT * FROM tasks WHERE goal_id = %s ORDER BY created_at ASC;", (goal[0],))
            tasks.extend(goal_tasks)
    #else:
    #    for goal in goals:
    #        goal_tasks = database.execute_query("SELECT * FROM tasks WHERE goal_id = %s AND DATE(due_date) = DATE(now()) ORDER BY created_at ASC;", (goal[0],))
    #        tasks.extend(goal_tasks)

    # sort tasks by their due date
    tasks.sort(key=lambda x: x[5])  # Sort tasks by due date

    # render the tasks page
    return render_template('my_tasks.html', user=user, tasks=tasks)

# Task Complete
@app.route('/my/tasks/<task_id>/complete')
def my_tasks_complete(task_id):
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get the task object
    task = database.execute_query("SELECT * FROM tasks WHERE id = %s;", (task_id,))

    # check if the task exists
    if len(task) == 0:
        # if not, return 404
        return jsonify({"error": "Task not found"}), 404
    
    task = task[0]

    # get the parent goal of the task
    goal = database.execute_query("SELECT * FROM goals WHERE id = %s AND user_id = %s;", (task[1], user[0]))

    # check if the goal exists and belongs to the user
    # on second thoughts, why don't we check if the user owns the object they're inspecting elsewhere? too late now ig...
    if len(goal) == 0 or user[0] != goal[0][1]:
        return redirect('/accounts/logout')
    
    # if the task is a milestone, advance the goal to the next stage
    if task[8]:
        # whoa boy. i sure hope this makes sense to somebody
        if goal[0][5] + 1 < len(json.loads(goal[0][6])["stages"]): # if not last stage

            # advance the goal to the next stage
            try: database.execute_command("UPDATE goals SET stage = stage + 1 WHERE id = %s;", (goal[0][0],))

            except Exception as e:

                # if there was some type of error, log it and return an error? i'm not very consistent with error handling and checking lol
                log.error(f"Error advancing goal stage: {e}")
                return redirect('/my/tasks?error=Error completing task.')
            
            # add to the task_queue here? i might be italian the amount of spaghetti code i wrote holy moly
            task_queue.put({"type": "create_stage_tasks", "data": {"goal_id": goal[0][0]}})
        
        # this is so nested i can barely figure out what the hell is going on
        # if the stage *is* the last stage, and the milestone is complete, the goal is complete
        else:
            log.info(f"Goal {goal[0][0]} completed!")

            # delete the tasks from the goal (again with the inconsistent error handling)
            database.execute_command("DELETE FROM tasks WHERE goal_id = %s;", (goal[0][0],))
            
            # redirect to a generic "goal complete" page cause i was to lazy to make it dynamic
            return redirect('/my/goals/complete')

    # finally, back to when it's *not* a milestone
    # mark the task as complete
    try: database.execute_command("UPDATE tasks SET status = %s WHERE id = %s;", ('complete', task_id))
    except Exception as e:
        # .. and if there was an error for some reason or another, log it and return an error
        log.error(f"Error completing task: {e}")
        return redirect('/my/tasks?error=Error completing task.')
    
    # redirect back to the tasks page
    return redirect('/my/tasks')

# Task Skip
@app.route('/my/tasks/<task_id>/skip')
def my_tasks_skip(task_id):
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # fairly similar to the my_tasks_complete function, i'm not repeating myself sorry

    task = database.execute_query("SELECT * FROM tasks WHERE id = %s;", (task_id,))
    if len(task) == 0:
        return jsonify({"error": "Task not found"}), 404
    task = task[0]
    goal = database.execute_query("SELECT * FROM goals WHERE id = %s AND user_id = %s;", (task[1], user[0]))
    if len(goal) == 0 or user[0] != goal[0][1]:
        return redirect('/accounts/logout')
    try: database.execute_command("UPDATE tasks SET status = %s WHERE id = %s;", ('skipped', task_id))
    except Exception as e:
        log.error(f"Error skipping task: {e}")
        return redirect('/my/tasks?error=Error skipping task.')
    return redirect('/my/tasks')

# Create Goal (/my/goals/create)
@app.route('/my/goals/create', methods=["GET", "POST"])
def my_goals_create():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    if request.method == 'POST':
        
        # get form data
        title = request.form.get('title')
        description = request.form.get('description')
        config = {"stages": json.loads(request.form.get('stages'))} # quick workaround

        # attempt to create the goal
        try: database.execute_command("INSERT INTO goals (user_id, title, description, created_at, stage, config) VALUES (%s, %s, %s, %s, %s, %s);", (user[0], title, description, datetime.datetime.now(), 0, json.dumps(config)))
        except Exception as e:
            # if an error occurred, log it and return an error
            log.error(f"Error creating goal: {e}")
            return render_template('my_goals_create.html', user=user, error="Error creating goal.")
        
        # get the id of the newly created goal
        id = database.execute_query("SELECT id FROM goals WHERE user_id = %s AND title = %s ORDER BY created_at DESC LIMIT 1;", (user[0], title))[0][0]

        # tell the task runner to create the tasks for this goal
        task_queue.put({"type": "create_stage_tasks", "data": {"goal_id": id}})

        # redirect to the goal details page
        return redirect('/my/goals/' + str(id))
    
    # render the create goal form
    return render_template('my_goals_create.html', user=user)

# Edit Goal (/my/goals/<goal_id>/edit)
@app.route('/my/goals/<goal_id>/edit', methods=["GET", "POST"])
def my_goals_edit(goal_id):
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get the goal to edit
    goal = database.execute_query("SELECT * FROM goals WHERE id = %s AND user_id = %s;", (goal_id, user[0]))

    # verify that the goal exists and belongs to the user
    if len(goal) == 0 or user[0] != goal[0][1]:
        return redirect('/accounts/logout')
    
    goal = goal[0] # small bug with the database module. see the database module for more info

    # if submitting the edit form
    if request.method == 'POST':

        # get form data
        title = request.form.get('title')
        description = request.form.get('description')
        config = {"stages": json.loads(request.form.get('stages'))} # quick workaround

        # attempt to update the goal
        try: database.execute_command("UPDATE goals SET title = %s, description = %s, config = %s WHERE id = %s AND user_id = %s;", (title, description, json.dumps(config), goal_id, user[0]))
        except Exception as e:
            # on error for whatever reason, log it and return an error
            log.error(f"Error updating goal: {e}")
            return render_template('my_goals_edit.html', user=user, goal=goal, error="Error updating goal.")
        
        id = goal[0] # get the goal id

        # tell the task runner to recreate the tasks for this goal
        task_queue.put({"type": "create_stage_tasks", "data": {"goal_id": id}})

        # redirect to the goal details page
        return redirect('/my/goals/' + str(id))
    
    # render the edit goal form
    return render_template('my_goals_edit.html', user=user, goal=goal)

# Delete Goal (/my/goals/<goal_id>/delete)
@app.route('/my/goals/<goal_id>/delete')
def my_goals_delete(goal_id):
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # get the goal to delete
    goal = database.execute_query("SELECT * FROM goals WHERE id = %s AND user_id = %s;", (goal_id, user[0]))

    # verify that the goal exists and belongs to the user
    if len(goal) == 0 or user[0] != goal[0][1]:
        return redirect('/accounts/logout')
    
    goal = goal[0] # small bug with the database module. see the database module for more info

    # attempt to delete the goal and its tasks
    try: 
        database.execute_command("DELETE FROM tasks WHERE goal_id = %s;", (goal_id,))
        database.execute_command("DELETE FROM goals WHERE id = %s AND user_id = %s;", (goal_id, user[0]))
    except Exception as e:
        # on error for whatever reason, log it and return an error
        log.error(f"Error deleting goal: {e}")
        return render_template('my_goals_goal.html', user=user, goal=goal, error="Error deleting goal.")
    
    # redirect to the goals page
    return redirect('/my/goals')

# My Goals Complete (/my/goals/complete)
@app.route('/my/goals/complete')
def my_goals_complete():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    
    # generic goal complete page i'm sorry :(
    return render_template('my_goals_complete.html', user=user)

# Misc
# Index (/)
@app.route('/')
def index():
    if auth(request)[0]:
        return redirect('/my/dashboard')
    
    # render the index page
    return render_template('misc_index.html')

# About (/about)
@app.route('/about')
def about():

    # we didn't actually build this page... awkward
    return render_template('misc_about.html')

# Admin
# spoiler alert: none of these pages were built. no comments here

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

# 7. Task Runner
# hastily cobbled together lol
import threading
import queue
task_queue = queue.Queue()
def task_runner():
    log.info("[TaskRunner] Task runner init")
    while True:
        task = task_queue.get()
        log.info(f"[TaskRunner] Got task: {task}")
        # Tasks look a little something like this:
        # {"type": type, "data": data}
        # Each type of task has it's own data

        # Create tasks for stage
        if task["type"] == "create_stage_tasks":
            # god knows what this does. i was very tired when i wrote it
            goal_id = task["data"]["goal_id"]
            log.info("[TaskRunner] Creating weekly tasks")
            goal = database.execute_query("SELECT * FROM goals WHERE id = %s;", (goal_id,))
            goal = goal[0] if goal else False
            if not goal: log.error("[TaskRunner] Goal not found"); continue
            config = json.loads(goal[6])
            current_stage = config["stages"][goal[5]]
            tasks = current_stage["tasks"]
            days_until_next_sunday = ((7 - datetime.datetime.now().weekday()) % 7) - 1
            next_sunday = (datetime.datetime.now() + datetime.timedelta(days=days_until_next_sunday)).replace(hour=23, minute=59, second=59, microsecond=999999)
            x = 0
            for x in range(int(current_stage["duration"])):
                y = 0
                for y in range(7):
                    current_day = next_sunday + datetime.timedelta(days=y)
                    for task in tasks:
                        if task["type"] == "daily":
                            task["due_date"] = current_day
                            database.execute_command("INSERT INTO tasks (goal_id, title, description, created_at, due_date, optional) VALUES (%s, %s, %s, %s, %s, %s);", (goal_id, task["title"], task["description"], datetime.datetime.now(), task["due_date"], task.get("optional", False)))
                    if y==6: # end of week
                        for task in tasks:
                            if task["type"] == "weekly":
                                task["due_date"] = current_day
                                database.execute_command("INSERT INTO tasks (goal_id, title, description, created_at, due_date, optional) VALUES (%s, %s, %s, %s, %s, %s);", (goal_id, task["title"], task["description"], datetime.datetime.now(), task["due_date"], task.get("optional", False)))
                        if x+1 == current_stage["duration"]: # end of stage
                            for task in tasks:
                                if task.get("milestone", False):
                                    task["due_date"] = current_day
                                    database.execute_command("INSERT INTO tasks (goal_id, title, description, created_at, due_date, milestone) VALUES (%s, %s, %s, %s, %s, %s);", (goal_id, task["title"], task["description"], datetime.datetime.now(), task["due_date"], True))        
                next_sunday += datetime.timedelta(weeks=1)
            
            # milestone tasks
            #ms_due_date = next_sunday - datetime.timedelta(weeks=1) # revert the week added
            ms_due_date = next_sunday # end of the last week of the stage
            milestone_raw = current_stage.get("milestone")
            if milestone_raw:
                database.execute_command("INSERT INTO tasks (goal_id, title, description, created_at, due_date, milestone) VALUES (%s, %s, %s, %s, %s, %s);", (goal_id, milestone_raw[0], milestone_raw[1], datetime.datetime.now(), ms_due_date, True))

            log.info("[TaskRunner] Stage tasks created")

        task_queue.task_done()

        time.sleep(1) # Prevents 100% CPU usage

if __name__ == '__main__':
    log.info("Starting server...")
    
    # start the task runner thread
    task_thread = threading.Thread(target=task_runner, daemon=True)
    task_thread.start()

    # start the flask server
    app.run(host="0.0.0.0", port=config.get("port", 5000))