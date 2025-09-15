# Goalkeeper
> This project is still way in development. Go away.

Goalkeeper is a goal tracker designed to help you stay on top of your physical and mental health by setting and achieving goals. It's a submission to the [2025 Premier's Coding Challenge](https://education.qld.gov.au/about-us/events-awards/awards-competitions/premiers-coding-challenge) in the Year 9/10 Pairs Open Language category.

## Quickstart

Download this repository and open `example.config.json`. Rename it to `config.json` and edit the values to as you see fit. Note, keep the database values the same unless using your own database.

```
\> docker compose up -d
```
This will pull `postgres:latest`, `python:3.11-slim` and build `app` from `python:3.11-slim`. It will then expose the app on port :4377. Give it a few seconds to get the database sorted.

## Longstart (baremetal)

This guide won't go over installing postgres, but just make sure the values in `config.json` match the ones you set.

Download this repository and run
```
\> python3 -m pip install -r requirements.txt
```
This will install all the libraries used in this project.
You can now start the app with
```
\> python3 main.py
```


## Writeup

This project uses the following components

![Map of the project](/docs/assets/map.png)

- Python: main.py: This is the main script used in the app. It serves the webserver and contains the task runner
- Python Thread: main.py:task_runner: This is the task runner used to perform tasks that can happen outside of a web request. Usually I would run this in a seperate container, but due to time contraints, I wasn't able to achieve this.
- Docker: postgres database: This holds all the data for the app

### Database

Our database is split into three tables; the `users` table, the `tokens` table, the `goals` table and the `tasks` table. 

The `users` table stores all metadata related to the user, such as their username, email, name, tags, notifications and settings. This table also stores a hashed version of the password, along with the salt, for security reasons.

The `tokens` table stores the login tokens used to authenticate users. There is functionality, like naming and managing tokens built into the backend, but wasn't impletmented in the frontend.

The `goals` table store all the data for each goal set by the user. It hold it's title, description, the current stage, and a JSON configuration for the goal. Currently, the only implemented values inside of the configuration is the stages list, which contains templates for tasks used by each stage along with it's title, description, and duration.

The `tasks` table stores all tasks the have been set for the user. It contains a title, description, a created timestamp, a due timestamp, and a parent goal ID, along with flags for different types of tasks.

### Webserver

Our webserver runs on Flask, and is split into four different sections:
- `accounts`: Handles user authentication
- `misc`: Contains pages such as the base template, and the index page
- `my`: Contains most of the pages for the app, such as the dashboard, the goals tab and the tasks tab.
- `admin`: An unused endpoint that would have allowed a user with the admin tag to manipulate objects in the database

Authentication is handled through the module `auth.py`, a custom made authentication library I made for Flask that allows for quick authentication. For example, at the top of almost every endpoint (excluding `misc_index`, which doesn't require a login), is a quick 3 liner that checks if the user is logged in, and if not, sends them to the login page.

```
@app.route("/some_endpoint")
def some_endpoint():
    success, user = auth(request)
    if not success:
        return redirect('/accounts/login?next=' + request.path)
    ...
```

Database communication is handled through a small wrapper of the `psycopg2` library for the PostgreSQL database.

Configuraion loading is handled through a small custom library that takes the contents of config.json and verifies it's validity.

### Task runner

Originally, I was going to design the task runner for Goalkeeper based off of the task runner design I used in another one of my projects, [BattleStats](https://github.com/NotLawson/battlestats). It runs in a seperate Docker container, and uses the pub/sub functionality of the key/value database Redis.

However, when finding parts to simplify, I had to condense the task runner into main.py, where it runs in a seperate thread and communicates via the Queues Library.