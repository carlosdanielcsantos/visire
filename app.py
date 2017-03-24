from flask import Flask
from flask import render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
from cutter import video_cutter

app = Flask('cutter')

app.config["UPLOAD_FOLDER"] = "uploads"

@app.route("/")
def index():
    return redirect('static/index.html')

@app.route("/upload", methods=["POST"])
def upload():
    fileob = request.files["file2upload"]
    filepath = app.config["UPLOAD_FOLDER"]+'/'+secure_filename(fileob.filename)
    fileob.save(filepath)
    
    cut_file = video_cutter(filepath)
    
    return send_file(cut_file,
                     #mimetype='text/csv',
                     attachment_filename='result.mp4',
                     as_attachment=True)

app.run(debug=False)