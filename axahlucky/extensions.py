from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager, AnonymousUserMixin


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
debug = DebugToolbarExtension()
migrate = Migrate()
ckeditor = CKEditor()
moment = Moment()
csrf = CSRFProtect()
mail = Mail()

@login_manager.user_loader
def load_user(user_id):
    from axahlucky.models import User
    user = User.query.get(user_id)
    return user

login_manager.login_view = 'auth.login'
class Guest(AnonymousUserMixin):

    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False

login_manager.anonymous_user = Guest