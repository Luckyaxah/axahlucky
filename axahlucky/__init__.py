import os
import click

from flask import Flask, render_template
from flask_sqlalchemy import get_debug_queries

from axahlucky.settings import config, basedir
from axahlucky.extensions import db, bootstrap, debug, migrate, ckeditor, moment, csrf
from axahlucky.blueprints.main import main_bp
from axahlucky.models import Opinion, Keyword, OpinionKeywordMapping

import logging
from logging.handlers import RotatingFileHandler

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('axahlucky')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)

    return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    debug.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)


def register_commands(app):

    @app.cli.command()
    @click.option('--keyword', default=10)
    @click.option('--opinion', default=50)
    def forge(keyword, opinion):
        """Generate fake data."""
        from axahlucky.fakes import fake_keyword, fake_opinion

        db.drop_all()
        db.create_all()

        click.echo('Generating the keywords...')
        fake_keyword(keyword)

        click.echo('Generating the opinions...')
        fake_opinion(opinion)

        click.echo('Done.')

def register_errorhandlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Opinion=Opinion, Keyword=Keyword, OpinionKeywordMapping=OpinionKeywordMapping)

def register_template_context(app):
    pass


def register_logging(app):
    # class RequestFormatter(logging.Formatter):
    #     def format(self, record):
    #         record.url = request.url
    #         record.remote_addr = request.remote_addr
    #         return super(RequestFormatter, self).format(record)
        
    # request_formatter = RequestFormatter(
    #     '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    #     '%(levelname)s in %(module)s: %(message)s'
    # )
    # mail_handler.setFormatter(request_formatter)


    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/axahlog.log'),\
        maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)


def register_request_handlers(app):
    @app.after_request
    def query_profile(response):
        for q in get_debug_queries():
            if q.duration >= app.config['AXAHLUCKY_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response