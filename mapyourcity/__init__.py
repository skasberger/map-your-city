from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('../includes/flask.cfg', silent=True)
db = SQLAlchemy(app)

from mapyourcity import views, db, models