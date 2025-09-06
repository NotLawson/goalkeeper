from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('accounts_register.html')

app.run(debug=True)