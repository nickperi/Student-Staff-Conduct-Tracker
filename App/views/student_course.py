from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required

from.index import index_views

from App.controllers import (
    jwt_required,
    enroll,
    get_all_enrollments,
    get_all_students,
    get_all_courses,
    get_all_enrollments_json
)

student_course_views = Blueprint('student_course_views', __name__, template_folder='../templates')

@student_course_views.route('/student-courses', methods=['GET'])
def get_enrollments_page():
    enrollments = get_all_enrollments()
    students = get_all_students()
    courses = get_all_courses()
    return render_template('student_courses.html', enrollments=enrollments, students=students, courses=courses)

@student_course_views.route('/api/student-courses', methods=['GET'])
def get_enrollments_action():
    enrollments = get_all_enrollments_json()
    return jsonify(enrollments)

@student_course_views.route('/api/student-courses', methods=['POST'])
def enroll_endpoint():
    data = request.json
    enrollment = enroll(data['student_id'], data['course_id'])
    if enrollment:
        return jsonify({'message': f"student {data['student_id']} enrolled in course {data['course_id']}"})
    return jsonify({'message': f"student {data['student_id']} not enrolled in course {data['course_id']}"})

@student_course_views.route('/student-courses', methods=['POST'])
def enroll_action():
    data = request.form
    enrollment = enroll(data['student_id'], data['course_id'])
    if enrollment:
        flash(f"student {data['student_id']} enrolled in course {data['course_id']}")
    return redirect(url_for('student_course_views.get_enrollments_page'))
