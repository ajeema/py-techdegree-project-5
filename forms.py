from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError

import models

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


def title_exists(form, field):
    if models.Post.select().where(models.Post.title == field.data).exists():
        raise ValidationError("That title is already in use.")


class PostForm(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired(), title_exists])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = StringField("Tags", description="Separate Multiple tags with commas.")

