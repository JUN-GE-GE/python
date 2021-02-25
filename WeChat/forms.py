from flask_wtf import FlaskForm

from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length

from WeChat.models.user import User

class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    email = StringField("Email Address",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password Repeat",validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')    

def validate_username(self, username):
    user = user.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValueError('please user different username')

def validate_email(self, username):
    user = user.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValueError('please user different email adress')


class EditProfileForm(FlaskForm):
    about_me = TextAreaField('about me',validators=[Length(min=0,max=120)])
    submit = SubmitField('Save')

class ChatForm(FlaskForm):
    chat = TextAreaField('chat',validators=[DataRequired(),Length(min=0,max=140)])
    submit = SubmitField('Chat')

class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email Address",validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')    

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('You do not have for this email adress!')

class PasswordResetForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password Repeat",validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Submit')