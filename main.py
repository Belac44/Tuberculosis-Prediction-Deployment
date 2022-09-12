from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import IMAGES, UploadSet, configure_uploads
from forms import PatientDetails, ImageUpload, HospitalRegister, LogIn
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash, generate_password_hash
# from skimage import color
# from skimage import io
# import pickle
import os

photos = UploadSet("photos", IMAGES)
# model = pickle.load(open('model.pkl', 'rb'))


app = Flask(__name__)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)
Bootstrap(app)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = HospitalRegister()
    if form.validate_on_submit():
        pass
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogIn()
    if form.validate_on_submit():
        pass
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    pass

@app.route("/", methods=["GET", "POST"])
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
def upload_image():
    form = ImageUpload()
    if form.validate_on_submit() and 'photo' in request.files:
        filename = photos.save(form.photo.data)
        file_url = photos.path(filename=filename)
        return render_template('predict.html', url=file_url)
    return render_template("upload.html", form=form)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    url = request.args.get("url")
    return render_template("predict.html", url=url)

def process_image(img):
    img = io.imread(img)
    imgGray = color.rgb2gray(img)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
