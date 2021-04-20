

from datetime import datetime

from flask import current_app
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


from axahlucky.extensions import db


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime,  default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    okm = db.relationship('OpinionKeywordMapping', back_populates='opinion', cascade='all')

    def add_keyword(self, keyword):
        okm = OpinionKeywordMapping(opinion=self, keyword = keyword)
        db.session.add(okm)
        db.session.commit()

    def remove_keyword(self, keyword):
        okm = OpinionKeywordMapping.query.filter_by(opinion_id = self.id, keyword_id=keyword.id).first()
        if okm:
            db.session.delete(okm)
            db.session.commit()

class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), unique=True)
    create_time = db.Column(db.DateTime,  default=datetime.utcnow)

    okm = db.relationship('OpinionKeywordMapping', back_populates='keyword', cascade='all')


class OpinionKeywordMapping(db.Model):
    opinion_id = db.Column(db.Integer, db.ForeignKey('opinion.id'), primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'), primary_key=True)

    opinion = db.relationship('Opinion', back_populates='okm', lazy='joined')
    keyword = db.relationship('Keyword', back_populates='okm', lazy='joined')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()
    
    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL_ADDRESS']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'
    
    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and \
            permission in self.role.permissions



roles_permissions = db.Table('roles_permissions', \
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)

    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map={
            'Locked': ['BROWSE'],
            'User': ['BROWSE','SEARCH'],
            'Administrator': ['BROWSE','SEARCH','CREATE','EDIT','DELETE','ADMINISTER']
        }
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name = permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
            db.session.commit()
    
    @staticmethod
    def init_role_permission():
        for user in User.query.all():
            if user.role is None:
                if user.email in current_app.config['ADMIN_EMAIL_ADDRESS']:
                    user.role = Role.query.filter_by(name='Administrator').first()
                else:
                    user.role = Role.query.filter_by(name='User').first()
            db.session.add(user)
        db.session.commit()

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)

    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')



