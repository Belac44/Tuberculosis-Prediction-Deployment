from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FileField
from wtforms.validators import DataRequired

class PatientDetails(FlaskForm):
    name = StringField("Patient's Name:", validators=[DataRequired()])
    age = IntegerField("Patient's Age:", validators=[DataRequired()])
    gender = SelectField("Gender:",choices=[(0,"Male"), (1,"Female")], validators=[DataRequired()])
    image_id = StringField("Image ID:", validators=[DataRequired()])
    hospital = StringField("Hospital Name:", validators=[DataRequired()])
    submit = SubmitField("Next")

class ImageUpload(FlaskForm):
    image = FileField("Choose Image", validators=[DataRequired()])
    upload = SubmitField("Upload")