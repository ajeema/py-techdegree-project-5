from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email

import models


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class TagField(StringField):
    def _value(self):
        if self.data:
            return ", ".join([tag.name for tag in self.data])
        return ""

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(",")
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        existing_tags = models.Tag.select().where(models.Tag.name.in_(tag_names))
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        new_tags = [models.Tag(name=name) for name in new_names]
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []



class PostForm(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = TagField("ex. tag1, tag2, tag3")
