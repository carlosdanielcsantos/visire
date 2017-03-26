from flask import Flask, session, jsonify, url_for
from flask import render_template, redirect, send_file, send_from_directory
from werkzeug.utils import secure_filename
from cutter import video_cutter
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import RadioField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os, time

SECRET_KEY = 'unv93qr32rfvby'

class UploadForm(Form):
    videofile = FileField(validators=[FileRequired(),
                                      FileAllowed(['mp4',
                                                   'avi',
                                                   'mkv',
                                                   'flv'], 'Videos only!')])

class SettingsForm(Form):
    magnitude = RadioField('Intensity',
                           choices=[('0','Low'), ('1','Medium'), ('2','High')],
                           default='0')
    period = RadioField('Period',
                        choices=[('0','Short'), ('1','Medium'), ('2','Long')],
                        default='0')

app = Flask('cutter')
Bootstrap(app)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config.from_object(__name__)

filename = ''
filepath = ''
cutter = None

@app.route("/", methods=("GET", "POST",))
def index():
    uploadForm = UploadForm()
    settingsForm = SettingsForm()

    global filename, filepath, state, cutter

    if uploadForm.validate_on_submit():
        # get form data
        f = uploadForm.videofile.data

        # get filename
        filename = secure_filename(f.filename)

        # save file to uploads dir
        filepath = os.path.join('uploads', filename)
        f.save(filepath)

        # render settings
        return render_template('cut.html', form=settingsForm,
                               uploaded=filename)

    if settingsForm.validate_on_submit():
        magnitude = int(settingsForm.magnitude.data)
        period = int(settingsForm.period.data)

        cutter = video_cutter(filepath, magnitude, period)

        cutter.start()

        # return empty
        return ('', 204)

    return render_template('index2.html', form=uploadForm,
                           uploaded=filename)

@app.route('/_state', methods= ['GET'])
def _state():
    global cutter
    if cutter is not None:
        return jsonify(state=cutter.state)
    else:
        return jsonify(state="Waiting")

@app.route('/send_result', methods=("GET", "POST",))
def send_result():
    global cutter, state
    result = cutter.cut_filename

    print "Sending result..."
    state = 'Finished!'
    print os.path.split(result)[1]
    cutter.sent = True

    return send_file(result,
                 #mimetype='text/csv',
                 attachment_filename='result.mp4',
                 as_attachment=True)




app.run(debug=True)
