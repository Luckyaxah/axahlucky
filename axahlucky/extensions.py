from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
bootstrap = Bootstrap()
nav = Nav()
debug = DebugToolbarExtension()

topbar = Navbar('',
    View('Home', 'main.index'),
    View('Opinions', 'main.opinions'),
    View('Keywords','main.keywords'),
    View('Info', 'main.info')
)
nav.register_element('top', topbar)

