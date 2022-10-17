from flask import Flask, render_template, request, redirect, url_for, flash
from flask_uploads import IMAGES, UploadSet, configure_uploads
from forms import PatientDetails, ImageUpload, HospitalRegister, LogIn, StaffRegister, StaffLogin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from model_build import ModelBuild
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import smtplib
import random
import os

photos = UploadSet("photos", IMAGES)

app = Flask(__name__)

app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
app.config["SECRET_KEY"] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tb-hospital-data.db'

db = SQLAlchemy(app)
configure_uploads(app, photos)
Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    hospital = db.Column(db.String(500), unique=True, nullable=False)
    code = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Patient(db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    image_id = db.Column(db.String(250), nullable=False, unique=True)
    hospital = db.Column(db.String(500), nullable=False)


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(250), nullable=False)
    lname = db.Column(db.String(250), nullable=False)
    emailH = db.Column(db.String(250), nullable=False)
    emailP = db.Column(db.String(250), nullable=False)
    organization = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.create_all()
global file_url


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = HospitalRegister()
    if form.validate_on_submit():
        new_user = User(
            hospital=form.name.data,
            code=form.code.data,
            password=generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            pass
        login_user(new_user)
        return redirect(url_for('get_data'))
    return render_template("register.html", form=form)


@app.route("/staff-register")
def staff_register():
    form = StaffRegister()
    if form.validate_on_submit():
        send_email(form.emailH.data)
        if form.fpassword.data == form.lpassword.data:
            new_staff = Staff(
                fname=form.fname.data,
                lname=form.lname.data,
                emailP=form.emailP.data,
                emailH=form.emailH.data,
                password=generate_password_hash(form.fpassword.data, method='pbkdf2:sha256', salt_length=8),
                organization=form.organization.data
            )
            db.session.add(new_staff)
            try:
                db.session.commit()
            except IntegrityError:
                pass
            login_user(new_staff)
            return redirect(url_for('get_data'))
        else:
            flash("Passwords do no match")
    return render_template('staff_register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogIn()
    if form.validate_on_submit():
        user_available = User.query.filter_by(code=form.code.data).first()
        if user_available and check_password_hash(user_available.password, form.password.data):
            login_user(user_available)
            return redirect(url_for('get_data'))
        else:
            flash("Invalid Credentials")
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route("/staff-login", methods=["GET", "POST"])
def staff_login():
    form = StaffLogin()
    if form.validate_on_submit():
        email = form.email.data
        found_staff = Staff.query.filter_by(emailP=email).first()
        if found_staff and check_password_hash(found_staff.password, form.password.data):
            login_user(user_available)
            return redirect(url_for('get_data'))
        else:
            flash("Invalid Credentials")
            return redirect(url_for('staff_login'))

    return render_template('staff_login.html', form=form)


@app.route("/staff-dashboard", methods=["GET", "POST"])
def staff_dashboard():
    patient_data = Patient.query.all()
    form = StaffRegister()
    display = request.args.get('id')
    return render_template("staff-dashboard.html", data=patient_data, form=form, display=display)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# @app.route("staff-dashboards")
# def handle_click():


@app.route("/patient", methods=["GET", "POST"])
def get_data():
    form = PatientDetails()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        gender = form.gender.data
        image_id = form.image_id.data
        hospital = form.hospital.data
        new_patient = Patient(
            name=name,
            age=age,
            gender=gender,
            image_id=image_id,
            hospital=hospital
        )
        db.session.add(new_patient)
        try:
            db.session.commit()
        except IntegrityError:
            pass
        return redirect(url_for('upload_image', ids=image_id))

    return render_template("index.html", form=form)


@app.route("/image", methods=["GET", "POST"])
def upload_image():
    image_id = request.args.get('ids')
    print(image_id)
    form = ImageUpload()
    if form.validate_on_submit() and 'photo' in request.files:
        photos.save(form.photo.data)
        file_url = photos.path(filename=image_id)
        return redirect(url_for('predict', url=file_url))
    return render_template("upload.html", form=form)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    url_passed = request.args.get("url")
    model = ModelBuild()
    features = model.preprocess_image2(url_passed)
    prediction = model.predict(features)
    if prediction[0] > prediction[1]:
        result = (0, prediction[0])
    elif prediction[0] < prediction[1]:
        result = (1, prediction[1])
    else:
        result = None
    return render_template("predict.html", prediction=result, url=url_passed)


def send_email(send_to):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    conncetion.login(user=os.environ['Email'], password=os.environ["Password"])
    num = random.randint(100000, 999999)
    connection.sendmail(
        from_addr=os.environ["Email"],
        to_addrs=send_to,
        msg=f"Subject:Verification code\n\n {num} is your TB Web Verification Code\nCode expires in 60 seconds")
    conncetion.close()


# def verification(user_entry):
#     if user_entry == send_email():
#         return True
#     return False

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
