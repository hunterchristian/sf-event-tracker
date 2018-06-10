from flask import Flask

from .createDatabase import db

# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have a primary key column of type sqlalchemy.Integer or
#      type sqlalchemy.Unicode. 
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).
class Event(db.Model):
  """
  A table to store data on events that are happening in San Francisco
  """

  __tablename__ = 'events'
  id             = db.Column(db.Integer, primary_key=True)
  #link          = Column(String, unique=True)
  date           = db.Column(db.String)
  time           = db.Column(db.String)
  datetime_start = db.Column(db.String)
  datetime_end   = db.Column(db.String)
  description    = db.Column(db.String)
  price          = db.Column(db.String)