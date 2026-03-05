import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from dotenv import load_dotenv
load_dotenv()


from App.database import init_db
from App.config import DevelopmentConfig, ProductionConfig


from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views, setup_admin

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    
    if os.environ.get("ENV") == "PRODUCTION":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader

    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    app.app_context().push()
    return app