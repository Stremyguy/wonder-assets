from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, MultipleFileField, ValidationError
from wtforms.validators import DataRequired
from app.services import get_all_types
from werkzeug.utils import secure_filename

MODEL_EXTENSIONS = {"gltf", "glb", "obj", "fbx", "stl", "dae", "ply", "3ds"}


class ItemForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    item_url = FileField("Select Item file")
    type = SelectField(
        "Type",
        coerce=int,
        validators=[DataRequired()]
    )
    is_private = BooleanField("Private", default=False)
    show_meta = BooleanField("Show meta", default=True)
    can_download = BooleanField("Downloadable", default=True)
    submit = SubmitField("Submit")
    
    def __init__(self, *args: list, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.type.choices = [
            (t.id, t.name) for t in get_all_types()
        ]

    def validate_item_url(self, field) -> None:
        if field.data:
            filename = secure_filename(field.data.filename)
            
            if not filename:
                raise ValidationError("Invalid filename")

            ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
            if ext not in MODEL_EXTENSIONS:
                raise ValidationError(f"Unsupported file type. Supported formats: {', '.join(MODEL_EXTENSIONS)}")