from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput


class CategoryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    short_description = TextAreaField("Short description")
    full_description = TextAreaField("Full description")
    visible_to_roles = SelectMultipleField(
        "Visible to Roles",
        coerce=int,
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False))
    is_private = BooleanField("Private")
    is_testing = BooleanField("Test mode")
    submit = SubmitField("Submit")
