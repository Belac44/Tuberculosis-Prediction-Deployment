from flask import Flask, render_template, request, redirect, url_for
from forms import PatientDetails, ImageUpload
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = "AJ3IANWIDBGSU82HHTEV15SC534S"
Bootstrap(app)


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
        image = form.image.data
        return redirect(url_for('predict', image=image))

    return render_template("upload.html", form=form)

@app.route("/predict")
def predict():
    image = request.args.get('image')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")