from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required

from.index import index_views

from App.controllers import (
    jwt_required,
    add_course,
    get_all_courses,
    get_all_courses_json
)

course_views = Blueprint('course_views', __name__, template_folder='../templates')

@course_views.route('/courses', methods=['GET'])
def get_courses_page():
    courses = get_all_courses()
    return render_template('courses.html', courses=courses)

@course_views.route('/api/courses', methods=['GET'])
def get_courses_action():
    courses = get_all_courses_json()
    return jsonify(courses)

@course_views.route('/api/courses', methods=['POST'])
def add_course_endpoint():
    data = request.json
    add_course(data['code'], data['title'])
    return jsonify({'message': f"course {data['code']} added"})

@course_views.route('/courses', methods=['POST'])
def add_course_action():
    data = request.form
    flash(f"course {data['code']} created!")
    add_course(data['code'], data['title'])
    return redirect(url_for('course_views.get_courses_page'))
