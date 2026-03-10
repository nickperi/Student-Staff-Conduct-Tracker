from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    jwt_required,
    create_offering,
    get_all_offerings,
    get_all_offerings_json,
    get_all_courses,
    get_all_staff,
    get_course,
    get_staff
)

offering_views = Blueprint('offering_views', __name__, template_folder='../templates')

@offering_views.route('/offerings', methods=['GET'])
def get_offerings_page():
    offerings = get_all_offerings()
    courses = get_all_courses()
    staff_members = get_all_staff()
    return render_template('offerings.html', offerings=offerings, courses=courses, staff_members=staff_members, get_course=get_course, get_staff=get_staff)

@offering_views.route('/api/offerings', methods=['GET'])
def get_offerings_action():
    offerings = get_all_offerings_json()
    return jsonify(offerings)

@offering_views.route('/api/offerings', methods=['POST'])
def create_offering_endpoint():
    data = request.json
    offering = create_offering(data['staff_id'], data['course_id'], data['semester'])
    if offering:
        return jsonify({'message': f"offering for course {data['course_id']} created"})
    return jsonify({'message': f"offering for course {data['course_id']} not created"})

@offering_views.route('/offerings', methods=['POST'])
def create_offering_action():
    data = request.form
    offering = create_offering(data['staff_id'], data['course_id'], data['semester'])
    if offering:
        flash(f"offering for course {data['course_id']} created")
    return redirect(url_for('offering_views.get_offerings_page'))