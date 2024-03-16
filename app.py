import os
import pyodbc, struct
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

app = Flask(__name__)

configure_azure_monitor(connection_string='APPLICATIONINSIGHTS_CONNECTION_STRING')

# Use environment variable or a default value
# SQL_SERVER_URI = os.environ.get("SQLConnection", "sqlite:///test.db")

SQL_SERVER_URI = os.environ.get('SQLConnection')

app.config['SQLALCHEMY_DATABASE_URI'] = SQL_SERVER_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Task class for SQL Server
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # os.environ.get('PORT', 8000) is to dynamically set the port
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

