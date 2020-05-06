from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError

import models


class LoginForm(FlaskForm):
    """Default login form"""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class TagField(StringField):
    """Class to hold and specify a field for tags in formfield so we can store it uniquely"""
    def _value(self):
        if self.data:
            return ", ".join([tag.name for tag in self.data])
        return ""

    def get_tags_from_string(self, tag_string):
        """Taks tag input field that is a comma separate string and splits them"""
        raw_tags = tag_string.split(",")
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        existing_tags = models.Tag.select().where(models.Tag.name.in_(tag_names))
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])
        new_tags = [models.Tag(name=name) for name in new_names]
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        """extends built in process_formdata function"""
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

def title_exists(form, field):
    """Custom validator to check if the title field exists."""
    if models.Entry.select().where(models.Entry.title == field.data).exists():
        raise ValidationError("That title is already in use.")

class EntryForm(FlaskForm):
    """Default form to add new entries"""
    title = StringField("Enter Title", validators=[DataRequired(), title_exists])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = TagField("ex: batman, robin, superman")


class EditEntryForm(FlaskForm):
    """Form specifically for editing that removes the title check validator."""
    title = StringField("Enter Title", validators=[DataRequired()])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = TagField("ex: You know what to do...(i.e batman, robin)")
