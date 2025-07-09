from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (log_review, get_all_reviews, get_all_reviews_json, get_my_upvotes, get_all_students, jwt_required)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/reviews', methods=['GET'])
@jwt_required()
def get_review_page():
    reviews = get_all_reviews()
    students = get_all_students()
    upvotes = get_my_upvotes(jwt_current_user.id)
    return render_template('reviews.html', reviews=reviews, upvotes=upvotes, students=students)

@review_views.route('/api/reviews', methods=['GET'])
def get_review_action():
    reviews = get_all_reviews_json()
    return jsonify(reviews)

@review_views.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review_endpoint():
    data = request.json
    log_review(jwt_current_user.id, data['studentid'], data['text'])
    return jsonify({'message': f"review {data['text']} created"})

@review_views.route('/reviews', methods=['POST'])
@jwt_required()
def create_review_action():
    data = request.form
    flash(f"staff member {jwt_current_user.id} reviewed student {data['studentid']}!")
    log_review(jwt_current_user.id, data['studentid'], data['text'])
    return redirect(url_for('review_views.get_review_page'))
