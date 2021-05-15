from flask import Flask
from flask import Blueprint, render_template, request, redirect, url_for
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

todo = Blueprint('todo', __name__, template_folder='templates', static_folder='static')

from app import *
from app import mongo
 

@todo.route('/')
def index():
    tasks = mongo.db.task.find()

    return render_template('index.html', tasks=tasks)


@todo.route('/add', methods=['POST', 'GET'])
def add_todo():
    if request.method == 'POST':
        task = request.form['task']
        current_time = datetime.datetime.now()

        task = mongo.db.task.insert({'task': task, 'datetime': current_time, 'active': 1, 'complete': 0})

        return redirect(url_for('todo.index'))
    
    return render_template('index.html')


@todo.route('/<id>/update', methods=['PUT', 'GET', 'POST'])
def delete_todo(id):
    moved = mongo.db.task.update_one({'_id': ObjectId(id)}, {'$set':{'active': 0, 'complete': 1}})
    # task = mongo.db.task.delete_one({'_id':ObjectId(id)})
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


@todo.route('/active', methods=['GET'])
def active():
    if request.method == 'GET':
        get_active = mongo.db.task.find({'active': 1})
        print(get_active)

        return render_template('index.html', tasks=get_active)


@todo.route('/completed', methods=['GET'])
def completed():
    if request.method == 'GET':
        completed = mongo.db.task.find({'complete': 1})

        return render_template('index.html', tasks=completed)