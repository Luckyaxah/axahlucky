from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField


class EditOpinionForm(FlaskForm):
    title = StringField('Title', validators=[])
    keyword = SelectMultipleField('Keyword', validators=[], coerce=int)
    # from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
    # from axahlucky.models import Keyword
    # keyword1 = QuerySelectMultipleField(query_factory=lambda: Keyword.query,get_label='content', allow_blank=True)
    content = CKEditorField('content', validators=[])
    submit = SubmitField()

class EditKeywordForm(FlaskForm):
    content = StringField('Content', validators=[])
    submit = SubmitField()