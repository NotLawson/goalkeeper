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

The `tokens` table stores
