from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from axahlucky.models import User

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

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),\
        Regexp('^[a-zA-Z0-9]*$', message="The username should contain only a-z, A-Z and 0-9.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class ForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()