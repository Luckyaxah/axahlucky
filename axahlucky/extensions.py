from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_wtf import CSRFProtect
from flask_mail import Mail

db = SQLAlchemy()
bootstrap = Bootstrap()
debug = DebugToolbarExtension()
migrate = Migrate()
ckeditor = CKEditor()
moment = Moment()
csrf = CSRFProtect()
mail = Mail()
