from flask import flash, redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, verify_jwt_in_request, current_user
from flask_admin import Admin
from App.models import db, User, Staff, Student, Review, Upvote, Downvote
from App.controllers import get_all_staff, get_review, get_all_reviews
import logging

logger = logging.getLogger(__name__)

class AdminView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

    @jwt_required()
    def is_accessible(self):
        return current_user is not None and current_user.get_user_type() == "staff"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_views.index_page', next=request.url))
    
class StaffView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

    @jwt_required()
    def is_accessible(self):
        return current_user is not None and current_user.get_user_type() == "staff"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))
    

class StudentView(ModelView):
    column_list = ('id', 'username', 'user_type', 'score',)
    column_sortable_list = ('id', 'username', 'score',)

    @jwt_required()
    def is_accessible(self):
        return current_user is not None and current_user.get_user_type() == "staff"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))
    


class ReviewView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'staffid', 'studentid', 'text', 'num_upvotes', 'num_downvotes', 'created_at')
    form_columns = ('studentid', 'text')

    def create_model(self, form):
        from flask import current_app
        with current_app.app_context():
            try:
                verify_jwt_in_request()
                logger.info(f"Current user: {current_user.id}")

                if not current_user.is_authenticated:
                    return False

                # Ensure current_user.id is assigned to staff_id
                staff_id = current_user.id  
                student_id = form.studentid.data  # Get from form input
                text = form.text.data

                # Manually create the instance and assign required attributes
                model = self.model(staffid=staff_id, studentid=student_id, text=text)

                self.session.add(model)
                self.session.commit()

                get_all_reviews()
                db.session.commit()  # Save changes

                logger.info(f"Review logged: {model}")
                return model
            except Exception as e:
                self.session.rollback()
                logger.error(f"Error logging review: {e}")
                return False
    


    
class UpvoteView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'staffid', 'reviewid')
    form_columns = ('reviewid',)

    def create_model(self, form):
        from flask import current_app
        with current_app.app_context():
            try:
                verify_jwt_in_request()
                logger.info(f"Current user: {current_user.id}")

                if not current_user.is_authenticated:
                    return False

                # Ensure current_user.id is assigned to staff_id
                staff_id = current_user.id  
                review_id = form.reviewid.data  # Get from form input

                # Manually create the instance and assign required attributes
                model = self.model(staffid=staff_id, reviewid=review_id)

                self.session.add(model)
                self.session.commit()

                review = get_review(review_id)
                review.num_upvotes += 1
                get_all_staff()
                db.session.commit()  # Save changes

                logger.info(f"Upvote created: {model}")
                return model
            except Exception as e:
                self.session.rollback()
                logger.error(f"Error creating upvote: {e}")
                return False


    def delete_model(self, model):
        """Override delete to update Review when an upvote is deleted"""
        reviewid = model.reviewid  # Assuming Upvote.reviewid has a relationship with Review.id
        super().delete_model(model)  # Delete the upvote
        review = get_review(reviewid)
        review.num_upvotes -= 1  # Recalculate student score
        db.session.commit()  # Save changes


    @jwt_required()
    def is_accessible(self):
        return current_user is not None and current_user.get_user_type() == "staff"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))
    

class DownvoteView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'staffid', 'reviewid')
    form_columns = ('reviewid',)
   
    def create_model(self, form):
        from flask import current_app
        with current_app.app_context():
            try:
                verify_jwt_in_request()
                logger.info(f"Current user: {current_user.id}")

                if not current_user.is_authenticated:
                    return False

                # Ensure current_user.id is assigned to staff_id
                staff_id = current_user.id  
                review_id = form.reviewid.data  # Get from form input

                # Manually create the instance and assign required attributes
                model = self.model(staffid=staff_id, reviewid=review_id)

                self.session.add(model)
                self.session.commit()

                review = get_review(review_id)
                review.num_downvotes += 1
                get_all_staff()
                db.session.commit()  # Save changes

                logger.info(f"Downvote created: {model}")
                return model
            except Exception as e:
                self.session.rollback()
                logger.error(f"Error creating downvote: {e}")
                return False


    def delete_model(self, model):
        """Override delete to update downvotes when a downvote is deleted"""
        reviewid = model.reviewid  # Assuming Downvote.reviewid has a relationship with Review.id
        super().delete_model(model)  # Delete the downvote
        review = get_review(reviewid)
        review.num_downvotes -= 1
        db.session.commit()  # Save changes

    @jwt_required()
    def is_accessible(self):
        return current_user is not None and current_user.get_user_type() == "staff"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_page', next=request.url))
    

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))
    admin.add_view(StaffView(Staff, db.session))
    admin.add_view(StudentView(Student, db.session))
    admin.add_view(ReviewView(Review, db.session))
    admin.add_view(UpvoteView(Upvote, db.session))
    admin.add_view(DownvoteView(Downvote, db.session))
