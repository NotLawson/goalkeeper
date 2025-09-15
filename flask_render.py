from flask import Flask, render_template

# the old way to test a template. deprecated in favor of flask_render_2.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('misc_index.html')

app.run(debug=True)