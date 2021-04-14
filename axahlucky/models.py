from axahlucky.extensions import db


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    
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

    okm = db.relationship('OpinionKeywordMapping', back_populates='keyword', cascade='all')


class OpinionKeywordMapping(db.Model):
    opinion_id = db.Column(db.Integer, db.ForeignKey('opinion.id'), primary_key=True)
    keyword_id = db.Column(db.Integer, db.ForeignKey('keyword.id'), primary_key=True)

    opinion = db.relationship('Opinion', back_populates='okm', lazy='joined')
    keyword = db.relationship('Keyword', back_populates='okm', lazy='joined')



