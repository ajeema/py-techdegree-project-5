from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])



def validate_title(FlaskForm, field):
    import models
    post = models.Post.get(title=field.data)
    if field.data == post.title:
        raise ValidationError(u"OOPS...That Title '{}' is taken!!!".format(post.title))


class PostForm(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired(), validate_title])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = StringField("Tags", description="Separate Multiple tags with commas.")
