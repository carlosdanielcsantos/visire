from flask import Flask
from flask import render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename
from cutter import video_cutter
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import RadioField
from wtforms.validators import DataRequired
import os

SECRET_KEY = '98un0vu9390)#U$#=)unv93qr32rfvby'

class UploadForm(Form):
    videofile = FileField(validators=[FileRequired()])

class SettingsForm(Form):
    magnitude = RadioField('Intensity', choices=[(1,'Low'), (2,'Medium'), (3,'High')])
    period = RadioField('Period', choices=[(1,'Short'), (2,'Medium'), (3,'Long')])

app = Flask('cutter')

app.config["UPLOAD_FOLDER"] = "uploads"
app.config.from_object(__name__)


@app.route("/", methods=("GET", "POST",))
def index():

    settings = SettingsForm()
    uploadForm = UploadForm()
    filename = ''

    if uploadForm.validate_on_submit():
        f = uploadForm.videofile.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('uploads', filename))
        return render_template('cut.html', form=settings, uploaded=filename)

    return render_template('index2.html', form=uploadForm, uploaded=filename)


@app.route("/cut", methods=["POST"])
def cut():
    print "entered cut"

    
#    cut_file = video_cutter(filepath)
    
#    return send_file(cut_file,
#                     #mimetype='text/csv',
#                     attachment_filename='result.mp4',
#                     as_attachment=True)


app.run(debug=False)