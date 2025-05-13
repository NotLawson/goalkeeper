# Main Server File
import os, sys, time, json, datetime
from flask import Flask, request, jsonify, render_template, redirect, send_file, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

app.run(port=5000)