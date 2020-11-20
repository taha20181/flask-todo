from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config.from_object('config.Config')
mongo = PyMongo(app)

from app.views import todo

app.register_blueprint(todo)

if __name__ == "__main__":
    app.run(debug=True)