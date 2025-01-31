# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .student import student_views
from .staff import staff_views
from .upvote import upvote_views
from .index import index_views
from .auth import auth_views
from .admin import *


views = [user_views, student_views, staff_views, upvote_views, index_views, auth_views] 
# blueprints must be added to this list