from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, EmailField, FileField, SelectMultipleField, SubmitField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import DataRequired
from app.services import get_all_roles


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()], render_kw={"readonly": True})
    bio = StringField("Bio")
    roles = MultiCheckboxField("Roles", coerce=int)
    avatar = FileField("Profile picture", validators=[
        FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only!")
    ], render_kw={"accept": "image/*"})
    submit = SubmitField("Submit")

    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.roles.choices = [(role.id, role.name) for role in get_all_roles()]
