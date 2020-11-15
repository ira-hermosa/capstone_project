#---------------------------------------------------------------------------#
# Imports
#---------------------------------------------------------------------------#
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
import json


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_create_all():
    db.create_all()


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#


'''
Lesson Model
'''


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    lesson_title = Column(String)
    grade = Column(Integer)
    lesson_summary = Column(String)
    category = Column(Integer)

    def __init__(self, lesson_title, grade, lesson_summary, category):
        self.lesson_title = lesson_title
        self.grade = grade
        self.lesson_summary = lesson_summary
        self.category = category

    '''
  insert()
    inserts a new object into a database
  '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
  delete()
    delete an existing object in a database
  '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
  update()
    updates an existing object in a database
  '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'lesson_title': self.lesson_title,
            'grade': self.grade,
            'lesson_summary': self.lesson_summary,
            'category': self.category
        }

# def __repr__(self):
        # return json.dumps(self)


'''
Category Model
'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }

    '''
  insert()
    inserts a new object into a database
  '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
  delete()
    delete an existing object in a database
  '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
  update()
    updates an existing object in a database
  '''

    def update(self):
        db.session.commit()

    # # def __repr__(self):
    # #     return json.dumps(self)
