from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required

from.index import index_views

from App.controllers import (
    jwt_required,
    enroll,
    get_all_enrollments,
    get_all_students,
    get_all_offerings,
    get_all_enrollments_json,
    get_course,
    get_staff
)

enrollment_views = Blueprint('enrollment_views', __name__, template_folder='../templates')

@enrollment_views.route('/enrollments', methods=['GET'])
def get_enrollments_page():
    enrollments = get_all_enrollments()
    students = get_all_students()
    offerings = get_all_offerings()
    return render_template('enrollments.html', enrollments=enrollments, students=students, offerings=offerings, get_course=get_course, get_staff=get_staff)

@enrollment_views.route('/api/enrollments', methods=['GET'])
def get_enrollments_action():
    enrollments = get_all_enrollments_json()
    return jsonify(enrollments)

@enrollment_views.route('/api/enrollments', methods=['POST'])
def enroll_endpoint():
    data = request.json
    enrollment = enroll(data['student_id'], data['offering_id'])
    if enrollment:
        return jsonify({'message': f"student {data['student_id']} enrolled in offering {data['offering_id']}"})
    return jsonify({'message': f"student {data['student_id']} not enrolled in offering {data['offering_id']}"})

@enrollment_views.route('/enrollments', methods=['POST'])
def enroll_action():
    data = request.form
    enrollment = enroll(data['student_id'], data['offering_id'])
    if enrollment:
        flash(f"student {data['student_id']} enrolled in offering {data['offering_id']}")
    return redirect(url_for('enrollment_views.get_enrollments_page'))
