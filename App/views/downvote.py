from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required

from.index import index_views

from App.controllers import (
    jwt_required,
    get_all_downvotes,
    get_all_downvotes_json,
    get_review,
    get_all_reviews,
    create_downvote,
    remove_downvote
)

downvote_views = Blueprint('downvote_views', __name__, template_folder='../templates')

@downvote_views.route('/downvotes', methods=['GET'])
def get_downvote_page():
    downvotes = get_all_downvotes()
    reviews = get_all_reviews()
    return render_template('downvotes.html', downvotes=downvotes, reviews=reviews)

@downvote_views.route('/api/downvotes', methods=['GET'])
def get_downvotes_action():
    downvotes = get_all_downvotes_json()
    return jsonify(downvotes)

@downvote_views.route('/api/downvotes', methods=['POST'])
@jwt_required()
def create_downvote_endpoint():
    data = request.json
    create_downvote(jwt_current_user.id, data['reviewid'])
    return jsonify({'message': f"staff {jwt_current_user.id} downvoted {data['reviewid']}"})

@downvote_views.route('/downvotes', methods=['POST'])
@jwt_required()
def create_downvote_action():
    data = request.json

    try: 
        create_downvote(jwt_current_user.id, data['reviewid'])
        flash(f"Staff member {jwt_current_user.id} downvoted Review {data['reviewid']}")
        review = get_review(data['reviewid'])
        redirect(url_for('downvote_views.get_downvote_page'))
        return jsonify({'success': True, 'message': 'Downvote successful!', 'num_downvotes': review.num_downvotes, 'num_upvotes': review.num_upvotes}), 200
    except Exception as e:
        print(f"Error: {e}")
        redirect(url_for('downvote_views.get_downvote_page'))
        return jsonify({'success': False, 'error': str(e)}), 500

@downvote_views.route('/downvotes/<int:reviewid>', methods=['DELETE'])
@jwt_required()
def remove_downvote_action(reviewid):
    downvote = remove_downvote(jwt_current_user.id, reviewid)
    review = get_review(reviewid)

    if downvote:
        return jsonify({'success': True, 'num_upvotes': review.num_upvotes, 'num_downvotes': review.num_downvotes})
    else:
        return jsonify({'success': False, 'error': 'Upvote not found'}), 404