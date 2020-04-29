from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = StringField('Tags', description="Separate Multiple tags with commas.")
