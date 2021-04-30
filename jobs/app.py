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

    cursor = connection.execute(sql, values)
    if commit:
        results = connection.commit()
    else:
        if single:
            results = cursor.fetchone()
        else:
            results = cursor.fetchall()
    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exeption):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@app.route('/jobs')
def jobs():
    
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


@app.route('/job/<job_id>')
def job(job_id):
    
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)


@app.route('/employer/<employer_id>')
def employer(employer_id):
    employer = execute_sql( 'SELECT * FROM employer WHERE id=?', [employer_id], single=True)

    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])

    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])

    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)