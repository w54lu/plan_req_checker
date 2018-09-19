from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Enroll
from app.course import schedule_by_class_number


class GetForm(FlaskForm):
    term = SelectField('Term', choices=[(1181, 'Winter 2018'), (1185, 'Spring 2018'), (1189, 'Fall 2018'), (1191, 'Winter 2019')])
    subject = SelectField('Subject Code', choices=[('CS', 'CS — Computer Science'), ('MATH', 'MATH — Mathematics'), ('STAT', 'STAT — Statistics')])
    catalog = StringField('Catalog Number')
    submit = SubmitField('Find')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    class_number = IntegerField('Class Number')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_class_number(self, class_number):
        enroll = Enroll.query.filter_by(class_number=class_number.data).first()
        if enroll:
            raise ValidationError('Class already added.')

        if schedule_by_class_number(class_number.data) == []:
            raise ValidationError('Invalid class number.')




