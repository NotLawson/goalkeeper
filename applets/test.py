#

name = 'Testing and stuff'
base = 'testing'

from flask import render_template

from __main__ import database, core, log

def function_name():
    return render_template('Testing/index.html')