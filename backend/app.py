#--------------------------------------------------------------------------#
# Imports
#--------------------------------------------------------------------------#
import os
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
import random
from sqlalchemy import exc
from models import db_create_all, setup_db, Lesson, Category
from auth import AuthError, requires_auth


#---------------------------------------------------------------------------#
# Pagination
#---------------------------------------------------------------------------#

LESSONS_PER_PAGE = 5


def paginate_lessons(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * LESSONS_PER_PAGE
    end = start + LESSONS_PER_PAGE

    lessons = [lesson.format() for lesson in selection]
    current_lessons = lessons[start:end]

    return current_lessons


#---------------------------------------------------------------------------#
# App set up
#---------------------------------------------------------------------------#

# def create_app(test_config=None):
app = Flask(__name__)
setup_db(app)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization, true')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, PUT, POST, DELETE, PATCH, OPTIONS')
    return response


db_create_all()

#----------------------------------------------------------------------------#
# Endpoints
#----------------------------------------------------------------------------#

# Get request for all available categories


@app.route('/categories')
def get_categories():

    categories = Category.query.order_by(Category.type).all()

    if len(categories) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories}
    })


# Get request for all available lessons
@app.route('/lessons')
def get_lessons():

    selection = Lesson.query.order_by(Lesson.id).all()
    current_lessons = paginate_lessons(request, selection)

    if len(current_lessons) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'lessons': current_lessons,
        'total_lessons': len(Lesson.query.all())
    })


# Get request for lessons by category
@app.route('/categories/<int:id>/lessons')
def get_lessons_by_category(id):

    try:
        category = Category.query.filter_by(id=id).one_or_none()

        if category is None:
            abort(404)

        lessons = Lesson.query.filter_by(category=id).all()
        current_lessons = paginate_lessons(request, lessons)

        return jsonify({
            'success': True,
            'lessons': current_lessons,
            'total_lessons': len(lessons),
            'current_categories': category.type
        })

    except Exception:
        abort(404)


# Post request to create a new category
@app.route('/categories', methods=['POST'])
@requires_auth('post:categories')
def create_new_category(token):
    body = request.get_json()

    new_type = body.get('type', None)

    if not('type' in body):
        abort(422)

    try:
        category = Category(type=new_type)
        category.insert()

        return jsonify({
            'success': True,
            'created': category.id,
            'total_categories': len(Category.query.all())
        })

    except Exception:
        abort(422)


# Post request to create a new lesson
@app.route('/lessons', methods=['POST'])
@requires_auth('post:lessons')
def create_new_lesson(token):
    body = request.get_json()

    new_lesson_title = body.get('lesson_title', None)
    new_grade = body.get('grade', None)
    new_lesson_summary = body.get('lesson_summary', None)
    new_category = body.get('category', None)

    if not('lesson_title' in body and 'grade' in body and 'lesson_summary' in body and 'category' in body):
        abort(422)

    try:
        lesson = Lesson(
            lesson_title=new_lesson_title,
            grade=new_grade,
            lesson_summary=new_lesson_summary,
            category=new_category)
        lesson.insert()
        selection = Lesson.query.order_by(Lesson.id).all()
        current_lessons = paginate_lessons(request, selection)

        return jsonify({
            'success': True,
            'created': lesson.id,
            'lessons': current_lessons,
            'total_lessons': len(Lesson.query.all())
        })

    except Exception:
        abort(422)


# Patch request to update an existing lesson
@app.route('/lessons/<int:lesson_id>', methods=['PATCH'])
@requires_auth('patch:lessons')
def update_lesson_by_id(token, lesson_id):
    body = request.get_json()

    try:
        lesson = Lesson.query.filter(Lesson.id == lesson_id).one_or_none()
        if lesson is None:
            abort(404)

        if 'lesson_title' in body:
            lesson.lesson_title = str(body.get('lesson_title'))

        if 'grade' in body:
            lesson.grade = int(body.get('grade'))

        if 'lesson_summary' in body:
            lesson.lesson_summary = str(body.get('lesson_summary'))

        if 'category' in body:
            lesson.category = str(body.get('category'))

        lesson.update()
        updated_lesson = Lesson.query.filter_by(id=lesson_id).first()

        return jsonify({
            'success': True,
            'updated': lesson_id
        })

    except Exception:
        abort(422)


# Delete an existing lesson by id
@app.route('/lessons/<int:lesson_id>', methods=['DELETE'])
@requires_auth('delete:lessons')
def delete_lesson(token, lesson_id):

    try:
        lesson = Lesson.query.filter(Lesson.id == lesson_id).one_or_none()

        lesson.delete()
        selection = Lesson.query.order_by(Lesson.id).all()
        current_lessons = paginate_lessons(request, selection)

        return jsonify({
            'success': True,
            'deleted': lesson_id,
            'lessons': current_lessons,
            'total_lessons': len(Lesson.query.all())
        })

    except Exception:
        abort(422)


#----------------------------------------------------------------------------#
# Error handlers
#----------------------------------------------------------------------------#

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorised"
    }), 401


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

    # return app

# if __name__ == '__main__':
#    app.run()
