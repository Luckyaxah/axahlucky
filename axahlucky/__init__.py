import os
import click

from flask import Flask

from axahlucky.settings import config
from axahlucky.extensions import db, bootstrap, nav
from axahlucky.blueprints.main import main_bp
from axahlucky.models import Opinion, Keyword, OpinionKeywordMapping



def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('axahlucky')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_template_context(app)

    return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)


def register_commands(app):

    @app.cli.command()
    def forge():
        """Generate fake data."""
        from axahlucky.fakes import fake_keyword, fake_opinion

        db.drop_all()
        db.create_all()

        click.echo('Generating the keywords...')
        fake_keyword()

        click.echo('Generating the opinions...')
        fake_opinion()

        click.echo('Done.')

def register_errorhandlers(app):
    pass

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Opinion=Opinion, Keyword=Keyword, OpinionKeywordMapping=OpinionKeywordMapping)

def register_template_context(app):
    pass
