from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required

from.index import index_views

from App.controllers import (
    create_upvote,
    remove_upvote,
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
    flash(f"Staff member {jwt_current_user.id} upvoted Review {data['reviewid']}")
    return jsonify({'message': f"staff {jwt_current_user.id} upvoted {data['reviewid']}"})


@upvote_views.route('/upvotes', methods=['POST'])
@jwt_required()
def create_upvote_action():
    data = request.json

    try:
        create_upvote(jwt_current_user.id, data['reviewid'])
        flash(f"Staff member {jwt_current_user.id} upvoted Review {data['reviewid']}")
        redirect(url_for('upvote_views.get_upvote_page'))
        return jsonify({'success': True, 'message': 'Upvote successful!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        redirect(url_for('upvote_views.get_upvote_page'))
        return jsonify({'success': False, 'error': str(e)}), 500


@upvote_views.route('/upvotes/<int:reviewid>', methods=['DELETE'])
@jwt_required()
def remove_upvote_action(reviewid):
    upvote = remove_upvote(jwt_current_user.id, reviewid)

    if upvote:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Upvote not found'}), 404


