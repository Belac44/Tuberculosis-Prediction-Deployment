from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired, regexp
import re

class PatientDetails(FlaskForm):
    name = StringField("Patient's Name:", validators=[DataRequired()])
    age = IntegerField("Patient's Age:", validators=[DataRequired()])
    gender = SelectField("Gender:",choices=[(0,"Male"), (1,"Female")], validators=[DataRequired()])
    image_id = StringField("Image ID:", validators=[DataRequired()])
    hospital = StringField("Hospital Name:", validators=[DataRequired()])
    submit = SubmitField("Next")

class ImageUpload(FlaskForm):
    image = FileField(u"Choose Image", [regexp(r'^[^/\\]\.jpg$'), DataRequired()])
    upload = SubmitField("Upload")

    def validate_image(FlaskForm, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)