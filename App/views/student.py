from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_student, 
    get_all_students,
    get_all_students_json,
    sort_students_by_id,
    sort_students_by_score,
    sort_students_by_username,
    jwt_required
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/students', methods=['GET'])
def get_student_page():
    students = get_all_students()
    return render_template('students.html', students=students)

@student_views.route('/view-students', methods=['GET'])
def get_students_sorted():
    students = get_all_students()
    return render_template('sort_students.html', students=students)

@student_views.route('/api/students', methods=['GET'])
def get_students_action():
    students = get_all_students_json()
    return jsonify(students)

@student_views.route('/api/students', methods=['POST'])
def create_student_endpoint():
    data = request.json
    create_student(data['username'], data['password'], data['email'])
    return jsonify({'message': f"student {data['username']} created"})

@student_views.route('/students', methods=['POST'])
def create_student_action():
    data = request.form
    flash(f"Student {data['username']} created!")
    create_student(data['username'], data['password'], data['email'])
    return redirect(url_for('student_views.get_student_page'))

@student_views.route('/api/students/sort-by-id-asc')
def get_students_by_id_asc():
    students = sort_students_by_id(ascending=True)
    return jsonify(students)

@student_views.route('/api/students/sort-by-id-desc')
def get_students_by_id_desc():
    students = sort_students_by_id(ascending=False)
    return jsonify(students)

@student_views.route('/api/students/sort-by-username-asc')
def get_students_by_username_asc():
    students = sort_students_by_username(ascending=True)
    return jsonify(students)

@student_views.route('/api/students/sort-by-username-desc')
def get_students_by_username_desc():
    students = sort_students_by_username(ascending=False)
    return jsonify(students)

@student_views.route('/api/students/sort-by-score-asc')
def get_students_by_score_asc():
    students = sort_students_by_score(ascending=True)
    return jsonify(students)

@student_views.route('/api/students/sort-by-score-desc')
def get_students_by_score_desc():
    students = sort_students_by_score(ascending=False)
    return jsonify(students)