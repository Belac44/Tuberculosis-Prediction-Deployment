from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from forms import PatientDetails, ImageUpload
from flask_bootstrap import Bootstrap
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "AJ3IANWIDBGSU82HHTEV15SC534S"
Bootstrap(app)
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

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
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        return render_template(url_for('predict', url=file_url))


    return render_template("upload.html", form=form)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    file_url = request.args.get("url")
    print(file_url)
    return render_template("predict.html", url=file_url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")