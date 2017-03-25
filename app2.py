from flask import Flask, session
from flask import render_template, redirect, send_file, send_from_directory
from werkzeug.utils import secure_filename
from cutter import video_cutter
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import RadioField
from wtforms.validators import DataRequired
import os

SECRET_KEY = 'unv93qr32rfvby'

class UploadForm(Form):
    videofile = FileField(validators=[FileRequired()])

class SettingsForm(Form):
    magnitude = RadioField('Intensity',
                           choices=[('0','Low'), ('1','Medium'), ('2','High')],
                           default='0')
    period = RadioField('Period',
                        choices=[('0','Short'), ('1','Medium'), ('2','Long')],
                        default='0')

app = Flask('cutter')

app.config["UPLOAD_FOLDER"] = "uploads"
app.config.from_object(__name__)

filename = ''; filepath = ''

@app.route("/", methods=("GET", "POST",))
def index():
    global filepath, filename
    state = 'Waiting'
    
    uploadForm = UploadForm()
    settingsForm = SettingsForm()

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
                               uploaded=filename, state=state)


    if settingsForm.validate_on_submit():
        magnitude = int(settingsForm.magnitude.data)
        period = int(settingsForm.period.data)

        state = 'Starting...'
        result = video_cutter(filepath, magnitude, period)
        state = 'Finished!'
        print os.path.split(result)[1]

        return send_file(result,
                     #mimetype='text/csv',
                     attachment_filename='result.mp4',
                     as_attachment=True)
        #return redirect('')
        #return send_from_directory('/uploads', os.path.split(result)[1],
        #                               as_attachment=True)

    return render_template('index2.html', form=uploadForm, uploaded=filename,
                           state=state)


@app.route("/cut", methods=["POST"])
def cut():
    print settings.magnitude.data
    print settings.period.data

    cut_file = video_cutter(filepath)

    return send_file(cut_file,
                     #mimetype='text/csv',
                     attachment_filename='result.mp4',
                     as_attachment=True)


@app.route('/uploads/<filename>')
def serve_file(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'uploads'), filename)

app.run(debug=False)
