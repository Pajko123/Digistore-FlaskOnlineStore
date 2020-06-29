from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, validators, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from digistore.models import User, Category, Post
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is allready used. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is allready used. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')



def choise_query():
	return Category.query

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Discription', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Software','Software'), ('Web Applications', 'Web Applications'),
     ('Games', 'Games'), ('Movies', 'Movies'), ('eBooks', 'eBooks'), ('Videos', 'Videos'), ('AudioMusic', 'AudioMusic'),
     ('Photography', 'Photography'), ('GraphicDigitalArt', 'GraphicDigitalArt'), ('DocumentsGuides', 'DocumentsGuides'),
     ('Courses','Courses'),('ProfessionalServices','ProfessionalServices'),('VirtualTickets','VirtualTickets')])
    price = FloatField('Price', validators=[DataRequired()])
    contact=TextAreaField('Enter your phone number! (Not required)')
    picture = FileField('Add a picture for your product', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    file_upload = FileField('Upload the file you want to sell!', validators=[FileAllowed(['txt', 'pdf', 'png', 'jpg',
    'jpeg', 'gif','png', 'zip', 'rar', '7zip', 'mp4', 'mov','wmv','wav', 'flv', 'avi', 'eps','epsi','epsf','psd','tif',])])
    
    submit = SubmitField('Sell')
