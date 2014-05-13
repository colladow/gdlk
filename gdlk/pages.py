from flask import render_template, url_for

from gdlk import app

@app.route('/')
def index():
    return render_template('index.html')
