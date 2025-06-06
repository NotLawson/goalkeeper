from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Testing/index.html', variable='words')

app.run(debug=True)