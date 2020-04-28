from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import (
    DataRequired,
    Email
)

from models import User



class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class PostForm(Form):
    title = StringField("Enter Title", validators = [DataRequired()])
    time_spent = IntegerField('How many Hours?', validators = [DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])

