from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required

from.index import index_views

from App.controllers import (
    create_upvote,
    get_all_upvotes,
    get_all_upvotes_json,
    get_all_reviews,
    jwt_required
)

upvote_views = Blueprint('upvote_views', __name__, template_folder='../templates')

@upvote_views.route('/upvotes', methods=['GET'])
def get_upvote_page():
    upvotes = get_all_upvotes()
    reviews = get_all_reviews()
    return render_template('upvotes.html', upvotes=upvotes, reviews=reviews)

@upvote_views.route('/api/upvotes', methods=['GET'])
def get_upvotes_action():
    upvotes = get_all_upvotes_json()
    return jsonify(upvotes)

@upvote_views.route('/api/upvotes', methods=['POST'])
@jwt_required()
def create_upvote_endpoint():
    data = request.json
    create_upvote(jwt_current_user.id, data['reviewid'])
    return jsonify({'message': f"staff {jwt_current_user.id} upvoted {data['reviewid']}"})

@upvote_views.route('/upvotes', methods=['POST'])
@jwt_required()
def create_upvote_action():
    data = request.form
    flash(f"Staff member {jwt_current_user.id} upvoted Review {data['reviewid']}")
    create_upvote(jwt_current_user.id, data['reviewid'])
    return redirect(url_for('upvote_views.get_upvote_page'))
