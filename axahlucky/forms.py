from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField


class EditOpinionForm(FlaskForm):
    title = StringField('Title', validators=[])
    keyword = SelectMultipleField('Keyword', validators=[], coerce=int)
    content = CKEditorField('content', validators=[])
    submit = SubmitField()

class EditKeywordForm(FlaskForm):
    content = StringField('Content', validators=[])
    submit = SubmitField()