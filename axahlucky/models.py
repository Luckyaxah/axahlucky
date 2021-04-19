

from datetime import datetime
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)



