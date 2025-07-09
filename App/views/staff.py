from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_staff,
    get_staff,
    get_staff_reviews,
    get_all_staff,
    get_all_staff_json,
    jwt_required
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff', methods=['GET'])
def get_staff_page():
    staff = get_all_staff()
    return render_template('staff.html', staff=staff)


@staff_views.route('/staff/<int:id>')
def my_page(id):
    staff = get_staff(id)
    reviews = get_staff_reviews(id)
    return render_template('staff_profile.html', staff=staff, reviews=reviews)


@staff_views.route('/api/staff', methods=['GET'])
def get_staff_action():
    staff = get_all_staff_json()
    return jsonify(staff)

@staff_views.route('/api/staff', methods=['POST'])
def create_staff_endpoint():
    data = request.json
    create_staff(data['username'], data['password'], data['email'])
    return jsonify({'message': f"staff member {data['username']} created"})

@staff_views.route('/staff', methods=['POST'])
def create_staff_action():
    data = request.form
    flash(f"Staff member {data['username']} created!")
    create_staff(data['username'], data['password'], data['email'])
    return redirect(url_for('staff_views.get_staff_page'))
