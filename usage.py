from flask_wtf import FlaskForm
from tag_list_field import TagListField

class Entry(FlaskForm):
    # other fields

    tags = TagListField(
        "Tags",
        separator=",",
        validators=[Length(max=8, message="You can only use up to 8 tags.")]
    )