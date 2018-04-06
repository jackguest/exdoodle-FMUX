from flask import Flask, request
from flask_restful import reqparse, abort, Resource
import json, threading, time
from bson.json_util import dumps, ObjectId
from pymongo import MongoClient

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.mongo_client = MongoClient('mongodb://0.0.0.0:27017')
        self.db = self.mongo_client.tviztest
    def run(self):
        print("Starting " + self.name)
        self.print_time(self.name, 5, self.counter)
        print("Exiting " + self.name)
    def print_time(self, threadName, counter, delay):
        while counter:
            if exitFlag:
                threadName.exit()
            time.sleep(delay)
            print("%s: %s" % (threadName, time.ctime(time.time())))
            self.db.test.insert_one({threadName: counter})
            counter -= 1


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 201

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def __init__(self, *urls, **kwargs):
        self.db = kwargs['db']
    def get(self):
        # Create new threads
        thread1 = myThread(1, "Thread-1", 1)
        thread2 = myThread(2, "Thread-2", 2)

        # Start new Threads
        thread1.start()
        thread2.start()

        print("Exiting Main Thread")

        return TODOS

    def post(self):
        args = json.loads(request.get_data().decode('utf-8'))
        #args = json.loads(request.get_data())
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
