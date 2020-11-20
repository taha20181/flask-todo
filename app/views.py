from flask import Flask
from flask import Blueprint, render_template, request, redirect, url_for
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

todo = Blueprint('todo', __name__, template_folder='templates', static_folder='static')

from app import *
 

@todo.route('/')
def index():
    tasks = mongo.db.task.find()

    return render_template('index.html', tasks=tasks)


@todo.route('/add', methods=['POST', 'GET'])
def add_todo():
    if request.method == 'POST':
        task = request.form['task']
        current_time = datetime.datetime.now()

        task = mongo.db.task.insert({'task': task, 'datetime': current_time})

        return redirect(url_for('todo.index'))
    
    return render_template('index.html')


@todo.route('/<id>/delete', methods=['DELETE', 'GET'])
def delete_todo(id):
    task = mongo.db.task.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('todo.index'))


def findTask(id):
    task = mongo.db.task.find_one({'_id': ObjectId(id)})

    return task


def getAllTasks():
    tasks = mongo.db.task.find()

    return tasks

@todo.route('/<id>/update', methods=['PUT'])
def update_todo(id):
    if request.method == 'PUT':
        task = request.form['task']
        current_time = datetime.datetime.now()
        task = mongo.db.task.update_one({'_id':ObjectId(id)}, {'task': task, 'datetime': current_time})

    return redirect(url_for('todo.index'))