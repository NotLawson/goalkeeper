from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('misc_index.html')

app.run(debug=True)