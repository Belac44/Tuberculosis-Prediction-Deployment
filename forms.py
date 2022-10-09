from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField, EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class PatientDetails(FlaskForm):
    name = StringField("Patient's Name:", validators=[DataRequired()])
    age = IntegerField("Patient's Age:", validators=[DataRequired()])
    gender = SelectField("Gender:", choices=[(0, "Male"), (1, "Female")], coerce=int, validators=[DataRequired()])
    image_id = StringField("Image ID:", validators=[DataRequired()])
    hospital = StringField("Hospital Name:", validators=[DataRequired()])
    submit = SubmitField("Next")


class ImageUpload(FlaskForm):
    photo = FileField(validators=[FileRequired('File was empty!')])
    upload = SubmitField("Upload")


class LogIn(FlaskForm):
    code = StringField("Hospital Code:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    login = SubmitField("Log In")


class HospitalRegister(FlaskForm):
    name = StringField("Hospital Name:", validators=[DataRequired()])
    code = StringField("Hospital Code:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    register = SubmitField("Register")

class StaffRegister(FlaskForm):
    fname = StringField("First Name:", validators=[DataRequired()])
    lname = StringField("Last Name:", validators=[DataRequired()])
    emailH = EmailField("Hospital Email:", validators=[DataRequired()])
    emailP = EmailField("Personal Email:", validators=[DataRequired()])
    fpassword = PasswordField("Password:", validators=[DataRequired()])
    lpassword = PasswordField("Confirm Password:", validators=[DataRequired()])
    organization = SelectField("Organization:", choices=[("Clinic"), ("Dispensary"), ("Hospital")])
    submit = SubmitField("Register")

class StaffLogin(FlaskForm):
    email = EmailField("Personal Email:")
    password = PasswordField("Password:")
    submit = SubmitField("Log In")