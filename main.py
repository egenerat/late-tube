from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template

import os
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True
app.secret_key = 'top_secret'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # TODO: Analysis here
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html', late_journeys=[
{
    'departure': 'Hammersmith',
    'destination': 'Hatton Cross',
    'estimated_delay': 45,
    'departure_date': '24th of July',
    'departure_time': '14:56'
},
{
    'departure': 'Picadilly Circus',
    'destination': 'Westminster',
    'estimated_delay': 36,
    'departure_date': '17th of August',
    'departure_time': '03:54'
}
])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()
