from flask import Blueprint, render_template, request, current_app, redirect, url_for
from axahlucky.models import Keyword, Opinion, OpinionKeywordMapping
from axahlucky.forms import EditOpinionForm, EditKeywordForm
from axahlucky.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/opinions')
def opinions():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['AXAHLUCKY_OPINION_PER_PAGE']
    
    pagination = Opinion.query.order_by(Opinion.update_time.desc()).paginate(page, per_page)
    opinions = pagination.items

    return render_template('main/opinions.html', opinions=opinions, pagination=pagination)

@main_bp.route('/keywords')
def keywords():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['AXAHLUCKY_KEYWORD_PER_PAGE']
    
    pagination = Keyword.query.order_by(Keyword.content.desc()).paginate(page, per_page)
    keywords = pagination.items

    return render_template('main/keywords.html', keywords=keywords, pagination=pagination)

@main_bp.route('/keywords/<int:keyword_id>')
def show_keyword(keyword_id):
    keyword = Keyword.query.get(keyword_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['AXAHLUCKY_KEYWORD_PER_PAGE']
    # way1
    # pagination = OpinionKeywordMapping.query.with_parent(keyword).paginate(page,per_page)
    # pagination = OpinionKeywordMapping.query.filter_by(keyword_id = keyword_id).paginate(page,per_page)
    # opinions = [item.opinion for item in pagination.items]

    # way2: use join
    pagination = Opinion.query.join(OpinionKeywordMapping, OpinionKeywordMapping.opinion_id == Opinion.id ).filter_by(keyword_id = keyword_id).order_by(Opinion.update_time.desc()).paginate(page,per_page)
    opinions = pagination.items
    return render_template('main/show_keyword.html', keyword=keyword, opinions = opinions, pagination = pagination)

@main_bp.route('/opinions/<int:opinion_id>')
def show_opinion(opinion_id):
    opinion = Opinion.query.get(opinion_id)
    okm_list = OpinionKeywordMapping.query.filter_by(opinion_id = opinion_id).all()
    keywords = [ i.keyword.content for i in okm_list]
    return render_template('main/show_opinion.html', opinion=opinion, keywords = keywords)

@main_bp.route('/opinions/<int:opinion_id>/edit', methods=['POST','GET'])
def edit_opinion(opinion_id):
    form = EditOpinionForm()
    opinion = Opinion.query.get_or_404(opinion_id)
    form.keyword.choices=[(keyword.id, keyword.content) for keyword in Keyword.query]

    if form.validate_on_submit():
        # okm_list = OpinionKeywordMapping.query.filter_by(opinion_id = opinion_id).all()
        opinion.title = form.title.data
        opinion.content = form.content.data
        
        keyword_ids = [ okm.keyword_id for okm in opinion.okm]

        for _id in set(form.keyword.data) - set(keyword_ids):
            okm = OpinionKeywordMapping(keyword_id = _id, opinion_id = opinion_id)
            db.session.add(okm)

        for _id in set(keyword_ids)- set(form.keyword.data):
            okm = OpinionKeywordMapping.query.filter_by(keyword_id = _id, opinion_id = opinion_id).first()
            db.session.delete(okm)

        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('.show_opinion', opinion_id=opinion_id))

    form.title.data = opinion.title
    form.keyword.data = [ okm.keyword_id for okm in opinion.okm]
    form.content.data = opinion.content
    return render_template('main/edit_opinion.html', form=form)

@main_bp.route('/opinions/new', methods=['POST','GET'])
def new_opinion():
    form = EditOpinionForm()
    form.keyword.choices=[(keyword.id, keyword.content) for keyword in Keyword.query]

    if form.validate_on_submit():
        opinion = Opinion(
            title = form.title.data,
            content = form.content.data
        )
        db.session.add(opinion)
        db.session.commit()

        for _id in set(form.keyword.data):
            okm = OpinionKeywordMapping(keyword_id = _id, opinion_id = opinion.id)
            db.session.add(okm)

        db.session.commit()
        return redirect(url_for('.show_opinion', opinion_id=opinion.id))
    return render_template('main/new_opinion.html', form=form)

@main_bp.route('/opinions/<int:opinion_id>/delete', methods=['POST'])
def delete_opinion(opinion_id):
    opinion = Opinion.query.get(opinion_id)
    if opinion:
        db.session.delete(opinion)
        db.session.commit()
    return redirect(url_for('.opinions'))

@main_bp.route('/keywords/new', methods=['POST','GET'])
def new_keyword():
    form = EditKeywordForm()

    if form.validate_on_submit():
        keyword = Keyword(
            content = form.content.data
        )
        db.session.add(keyword)
        db.session.commit()

        return redirect(url_for('.keywords'))
    return render_template('main/new_keyword.html', form=form)

@main_bp.route('/keywords/<int:keyword_id>/delete', methods=['POST'])
def delete_keyword(keyword_id):
    keyword = Keyword.query.get(keyword_id)
    if keyword:
        db.session.delete(keyword)
        db.session.commit()
    return redirect(url_for('.keywords'))



@main_bp.route('/info')
def info():
    return render_template('main/info.html')