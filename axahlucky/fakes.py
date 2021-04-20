import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from axahlucky.extensions import db
from axahlucky.models import Opinion, Keyword, OpinionKeywordMapping, User, Role

fake = Faker()

def fake_admin():
    admin = User(
        name = 'Admin',
        username = 'admin',
        email = 'admin@axahlucky.com',
        confirmed = True
    )
    admin.set_password('123456')
    role = Role.query.filter_by(name='Administrator').first()
    admin.role = role
    db.session.add(admin)
    db.session.commit()

def fake_user(count=5):
    for i in range(count):
        user = User(
            name = fake.name(),
            confirmed = True,
            username = fake.user_name(),
            member_since = fake.date_this_decade(),
            email = fake.email()
        )
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_keyword(count=5):

    for i in range(count):
        keyword = Keyword(
            content=fake.word()
        )
        db.session.add(keyword)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_opinion(count=50):
    keywords = Keyword.query.all()
    for i in range(count):
        opinion = Opinion(
            title = fake.sentence(),
            content = fake.sentence()
        )
        keyword = random.choice(keywords)
        opinion.add_keyword(keyword)
        db.session.add(opinion)
    db.session.commit()

# def fake_opinion_remove_keyword(count=1):
#     keywords = Keyword.query.all()
#     for i in range(count):
#         opinion = Opinion(
#             content = fake.sentence()
#         )
#         print(opinion.content)
#         keyword = random.choice(keywords)
#         opinion.add_keyword(keyword)
#         db.session.add(opinion)
#     db.session.commit()
#     opinion.remove_keyword(keyword)
