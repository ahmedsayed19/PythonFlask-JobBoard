from flask import render_template
from flask.app import Flask
app = Flask(__name__)

@app.route('/')
def jobs():
    return render_template('index.html')