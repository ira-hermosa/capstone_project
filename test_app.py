#-----------------------------------------------------------------#
# Imports
#-----------------------------------------------------------------#
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

# from app import create_app

from app import app

from models import setup_db, db_create_all, Lesson, Category


# -----------------------------------------------------------------
# Class for lesson test case
# -----------------------------------------------------------------

class LessonTestCase(unittest.TestCase):
    """This class represents the lesson test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "lessonplan"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'ira', 'ira', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.new_lesson = {
            'lesson_title': 'History New Project',
            'grade': 6,
            'lesson_summary': 'This is a new lesson plan summary',
            'category': 1
        }

        self.new_category = {
            'type': 'History'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# -------------------------------------------------------------------------
# Tests for successful operations and for expected errors
# --------------------------------------------------------------------------

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_non_existent_categories_404(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_paginated_lessons(self):
        res = self.client().get('/lessons')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_lessons'])
        self.assertTrue(data['lessons'])

    def test_get_non_existent_lesson_404(self):
        res = self.client().get('/lessons?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_lessons_by_category(self):
        res = self.client().get('/categories/1/lessons')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_categories'])

    def test_non_existent_category_id(self):
        res = self.client().get('categories/100/lessons')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_new_category(self):
        res = self.client().post('/categories', json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_categories'])

    def test_category_creation_not_allowed_401(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_add_new_lesson(self):
        res = self.client().post('/lessons', json=self.new_lesson)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['lessons']))

    def test_lesson_creation_not_allowed_401(self):
        res = self.client().post('/lessons')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_delete_lesson_by_id(self):
        res = self.client().delete('/lessons/1')
        data = json.loads(res.data)

        lesson = Lesson.query.filter(Lesson.id == 1). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(data['total_lessons'], len(Lesson.query.all()))

    def test_delete_lesson_401(self):
        res = self.client().delete('/lessons/25')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_update_lesson(self):
        res = self.client().patch('/lessons/1', json={'grade': 9})
        data = json.loads(res.data)

        lesson = Lesson.query.filter(Lesson.id == 1). one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(lesson.format()['grade'], 9)

    def test_401_unauthorised_update(self):
        res = self.client().patch('/lessons/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
