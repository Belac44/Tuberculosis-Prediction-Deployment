from flask import Flask, render_template, request, redirect, url_for, flash
from flask_uploads import IMAGES, UploadSet, configure_uploads
from forms import PatientDetails, ImageUpload, HospitalRegister, LogIn
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import os

photos = UploadSet("photos", IMAGES)
# model = pickle.load(open('model.pkl', 'rb'))


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
    id = db.Column(db.Integer, primary_key=True)
    hospital = db.Column(db.String(500), unique=True, nullable=False)
    code = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


db.create_all()
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@login_required
def get_data():
    form = PatientDetails()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        gender = form.gender.data
        image_id = form.image_id.data
        hospital = form.hospital.data

        return redirect(url_for('upload_image'))

    return render_template("index.html", form=form)


@app.route("/image", methods=["GET", "POST"])
@login_required
def upload_image():
    form = ImageUpload()
    if form.validate_on_submit() and 'photo' in request.files:
        filename = photos.save(form.photo.data)
        file_url = photos.path(filename=filename)
        return render_template('predict.html', url=file_url)
    return render_template("upload.html", form=form)


@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    url = request.args.get("url")
    return render_template("predict.html", url=url)

def process_image(img):
    img = io.imread(img)
    imgGray = color.rgb2gray(img)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
