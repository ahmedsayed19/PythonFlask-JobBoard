# from flask import render_template
from flask import Flask, render_template, g
import sqlite3

PATH = "db/jobs.sqlite"
# conn = sqlite3()
app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)
    if not connection:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()

    cursor = connection.execute()
    if commit:
        results = connection.commit()
    else:
        if single:
            results = cursor.fetchone()
        else:
            results = cursor.fetchall()
    return results

@app.teardown_appcontext
def close_connection(exeption):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')