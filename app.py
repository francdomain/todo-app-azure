# import os
# import pyodbc, struct
# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)


# # Use environment variable or a default value
# # SQL_SERVER_URI = os.environ.get("SQLConnection", "sqlite:///test.db")

# SQL_SERVER_URI = os.environ.get('SQLConnection')

# if SQL_SERVER_URI is None:
#     raise ValueError("SQLConnection environment variable is not set.")

# app.config['SQLALCHEMY_DATABASE_URI'] = SQL_SERVER_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define Task class for SQL Server
# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)

# @app.route('/')
# def index():
#     tasks = Task.query.all()
#     return render_template('index.html', tasks=tasks)

# @app.route('/add', methods=['POST'])
# def add():
#     content = request.form['content']
#     new_task = Task(content=content)
#     db.session.add(new_task)
#     db.session.commit()
#     return redirect(url_for('index'))

# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Task.query.get(id)
#     db.session.delete(task_to_delete)
#     db.session.commit()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(host='0.0.0.0', port=8000)
#     # app.run(debug=True)




import os
import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use environment variable or a default value
# SQL_SERVER_URI = os.environ.get("SQLConnection", "sqlite:///test.db")
SQL_SERVER_URI = os.environ.get("SQLConnection")

if SQL_SERVER_URI is None:
    raise ValueError("SQLConnection environment variable is not set.")

app.config['SQLALCHEMY_DATABASE_URI'] = SQL_SERVER_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Task class for SQL Server
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Set up logging
import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'log.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app.logger.addHandler(my_handler)

# Handle database connection errors
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    app.logger.error(f"Error creating database tables: {str(e)}")
    sys.exit(1)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    try:
        content = request.form.get('content', '')
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Error adding task: {str(e)}")
        return render_template('error.html', error_message="Error adding task")

@app.route('/delete/<int:id>')
def delete(id):
    try:
        task_to_delete = Task.query.get(id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Error deleting task: {str(e)}")
        return render_template('error.html', error_message="Error deleting task")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
