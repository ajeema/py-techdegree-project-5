from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError

import models


class LoginForm(FlaskForm):
    """Default login form"""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class FormTagField(StringField):
    """Class to hold and specify a field for tags in formfield so we can
    store it uniquely"""

    def _value(self):
        if self.data:
            return ", ".join([tag.name for tag in self.data])
        return ""

    def tags_form_input(self, tag_string):
        """Taks tag input field that is a comma separate string
        and splits them"""
        input_tags = tag_string.split(",")
        tag_label = [name.strip() for name in input_tags if name.strip()]
        tags = models.Tag.select().where(models.Tag.name.in_(tag_label))
        updated_label = set(tag_label) - set([tag.name for tag in tags])
        new_tags = [models.Tag(name=name) for name in updated_label]
        return list(tags) + new_tags

    def process_formdata(self, valuelist):
        """extends built in process_formdata function"""
        if valuelist:
            self.data = self.tags_form_input(valuelist[0])
        else:
            self.data = []


def title_exists(form, field):
    """Custom validator to check if the title field exists."""
    if models.Entry.select().where(models.Entry.title == field.data).exists():
        raise ValidationError("That title is already in use.")


class EntryForm(FlaskForm):
    """Default form to add new entries"""

    title = StringField("Enter Title",
                        validators=[DataRequired(), title_exists])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = FormTagField("ex: batman, robin, superman")


class EditEntryForm(FlaskForm):
    """Form specifically for editing that removes the title check validator."""

    title = StringField("Enter Title", validators=[DataRequired()])
    time_spent = IntegerField("How many Hours?", validators=[DataRequired()])
    content = TextAreaField("Enter text...", validators=[DataRequired()])
    resources = TextAreaField("Resources...", validators=[DataRequired()])
    tags = FormTagField("ex: You know what to do...(i.e batman, robin)")
