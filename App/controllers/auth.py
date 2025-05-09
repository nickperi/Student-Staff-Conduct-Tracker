from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User

def login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)  # Identity should always be a string (username)


def setup_jwt(app):
  jwt = JWTManager(app)
  
  # Ensure we consistently use username as identity
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user = User.query.filter_by(username=identity).one_or_none()
    if user:
      return user.username
    return None
    
  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # This is the username
    print("User Identity: " + identity)
    return User.query.filter_by(username=identity).one_or_none()
  return jwt


def add_auth_context(app):
  @app.context_processor
  def inject_user():
    try:
      verify_jwt_in_request()
      username = get_jwt_identity()  # Now it correctly retrieves the username
      current_user = User.query.filter_by(username=username).one_or_none()
      is_authenticated = current_user is not None
    except Exception as e:
      print(e)
      is_authenticated = False
      current_user = None
    return dict(is_authenticated=is_authenticated, current_user=current_user)
