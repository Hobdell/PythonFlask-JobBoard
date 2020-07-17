from flask import render_template, Flask, g
import sqlite3

PATH = 'db/jobs.sqlite'

app = Flask(__name__)


def open_connection():
    connection = g.__getattr__('_connection', None)
    if connection is None:
        connection, g.connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection


def execute_sql(sql, values: tuple = (), commit: bool = False, single: bool = False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit is True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results


@app.teardown_appcontext
def close_connection(exception):
    connection = g.__getattr__('_connection', None)
    if connection is not None:
        connection.close()


@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')
