import sys
# Include modules in parent directory (mainly for /database folder)
sys.path.append('/Users/hunterhodnett/PersonalProjects/sf-events-tracker')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

from database.createDatabase import db, app
from database.models import Event

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Event, methods=['GET'])

# start the flask loop
app.run()