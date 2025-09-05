from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('misc_base.html')

app.run(port=5001, debug=True)