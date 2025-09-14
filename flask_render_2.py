# render pages with example data for development

from flask import Flask, render_template, request
from datetime import datetime, timedelta
import json
app = Flask(__name__)

@app.context_processor
def inject_global_variables():
    return dict(
        datetime=datetime,
        timedelta=timedelta,
        int=int,
        str=str,
        len=len,
        enumerate=enumerate,
        round=round,
        load=json.loads,
    )

def example_data():
    example_user = [1, 'username', 'username@email.com', 'Example Username', 'password', 'salt', datetime.now() - timedelta(days=30), datetime.now(), {}, [{'id': 1, 'title': 'Example Notification', 'message': 'This is an example notification.', 'created_at': datetime.now() - timedelta(days=1), 'action': '/my/goals/1'}, {'id': 2, 'title': 'Another Notification', 'message': 'This is another example notification.', 'created_at': datetime.now() - timedelta(hours=5), 'action': '/my/tasks'}], ['user'], [2, 3]]
    example_goals = [
        [1, 1, 'Example Goal 1', 'This is an example goal description.', datetime.now() - timedelta(days=10), 1, json.dumps({'stages': [{'id': 1, 'title': 'Stage 1', 'description': 'This is stage 1.', 'tasks': [{'title': 'Task 1', 'description': 'This is task 1.', 'type': 'daily', 'optional': False}, {'title': 'Task 2', 'description': 'This is task 2.', 'type': 'weekly', 'optional': True}], 'milestone': 'Milestone 1', 'duration': 2}, {'id': 2, 'title': 'Stage 2', 'description': 'This is stage 2.', 'tasks': [{'title': 'Task 3', 'description': 'This is task 3.', 'type': 'monthly', 'optional': False}], 'milestone': 'Milestone 2', 'duration': 3}]}), None],
        [2, 1, 'Example Goal 2', 'This is another example goal description.', datetime.now() - timedelta(days=20), 1, json.dumps({'stages': [{'id': 1, 'title': 'Stage 1', 'description': 'This is stage 1.', 'tasks': [{'title': 'Task A', 'description': 'This is task A.', 'type': 'daily', 'optional': False}], 'milestone': 'Milestone A', 'duration': 4}]}), None]
    ]
    example_tasks = [
        [1, 1, 'Task 1', 'This task is part of Example Goal 1.', datetime.now() - timedelta(days=5), datetime.now() - timedelta(hours=5), 'incomplete', False, False, False],
        [2, 1, 'Task 2', 'This task is also part of Example Goal 1.', datetime.now() - timedelta(days=3), datetime.now() + timedelta(days=1), 'complete', True, False, False],
        [3, 2, 'Task 3', 'This task is part of Example Goal 2.', datetime.now() - timedelta(days=15), datetime.now() + timedelta(days=10), 'skipped', False, False, False]
    ]
    return example_user, example_goals, example_tasks

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'POST':
        print(f"Received POST request on {path} with form data: {request.form}")
        return render_template('misc_formDebug.html', form_data=request.form)
    example_user, example_goals, example_tasks = example_data()
    try:
        path = path.replace('/', '_')
        print(f"Rendering path: {path}.html")
        return render_template(path + '.html', user=example_user, goals=example_goals[:3], tasks=example_tasks[:3])
    except Exception as e:
        print(f"Error rendering {path}.html: {e}")
        return render_template('misc_notbuilt.html'), 404

def sort_goals(goal):
    return goal[4] # sort by created_at
def sort_tasks(task):
    return task[5] # sort by due_date


app.run(port=5001, debug=True)