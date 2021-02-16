from flask import Flask, render_template, redirect, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tables import Results, Explore, Reports, Paths
from werkzeug.utils import secure_filename
import os
import librosa, librosa.display # Librosa is a Python library that helps us work with audio data and display for visualization
import matplotlib.pyplot as plt 
import numpy as np 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Sounds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    sound_path = db.Column(db.String(400), nullable=False)
    waveform_path = db.Column(db.String(400), nullable=False)
    sampling_freq = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(200), nullable=False)
    file_duration = db.Column(db.Float,nullable=False)
    file_size = db.Column(db.Float, nullable=False)
    data = db.Column(db.LargeBinary)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Title %r>' %self.id

@app.route("/", methods = ['GET', 'POST'])
def home():
    playlist = os.listdir('static/music/')[:10]
    return render_template("home.html", playlist=playlist)
    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/explore")
def explore():
    sounds = Sounds.query.order_by(Sounds.date_uploaded)
    table1 = Explore(sounds)
    return render_template("explore.html", sounds=sounds, table1=table1)

@app.route("/download/<int:id>")
def download(id):
    list_to_download = Sounds.query.get_or_404(id)
    download_audio = "/home/azealiaa/flask_project/G2_PROJECT" + list_to_download.sound_path
    return send_file(download_audio, as_attachment=True)

@app.route("/show/<int:id>", methods = ['GET'])
def show(id):
    list_to_show = Sounds.query.get_or_404(id)
    playing = list_to_show.title
    image_display = list_to_show.waveform_path
    playlist = list_to_show.sound_path
    user = list_to_show.username
    location = list_to_show.location
    duration = round(list_to_show.file_duration,2)
    filesize = round(list_to_show.file_size,2)
    filetype = list_to_show.file_type 
    sampling = list_to_show.sampling_freq  
    download_id =  list_to_show.id
    return render_template("show.html", list_to_show = list_to_show, user=user, location=location, playing=playing, playlist=playlist, image_display=image_display, duration=duration, filetype=filetype, filesize=filesize, sampling=sampling, download_id=download_id)

@app.route("/delete/<int:id>")
def delete(id):
    list_to_delete = Sounds.query.get_or_404(id)
    path = "/home/azealiaa/flask_project/G2_PROJECT"
    sound = path + list_to_delete.sound_path
    image = path + list_to_delete.waveform_path
    os.remove(os.path.join(sound))
    os.remove(os.path.join(image))
    try:
        db.session.delete(list_to_delete)
        db.session.commit()
        return redirect('/database')
    except:
        return "There was a problem deleting"

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        if request.form['email'] == 'admin@bisori.my' and request.form['password'] == 'admin123':
            return redirect('/database')
        else:
            return "You are not allowed to view database"
    else:
        return render_template('login.html')

    
    
@app.route("/database", methods = ['POST', 'GET'])
def database():
    
    sounds = Sounds.query.order_by(Sounds.date_uploaded)
    table = Results(sounds)
    table.border = True

    table_path = Paths(sounds)
    table_path.border = True

    table_result = Reports(sounds)
    table_result.border = True

    return render_template("database.html", sounds=sounds, table=table, table_result=table_result, table_path=table_path)

@app.route("/confirm")
def confirm():
    
    return render_template("confirm.html")


@app.route("/upload", methods = ['POST', 'GET'])
def upload():
    db.create_all()
    
    if request.method == "POST":

        if request.files:

            audio = request.files['inputFile']
            audio_filename = request.form["filename"]
            filename = secure_filename(audio_filename)
            user = secure_filename(request.form["username"])
            audio.save(os.path.join("/home/azealiaa/flask_project/G2_PROJECT/static/music/" + user + "_" + filename))
            image_name = filename.split('.')
            image = "/home/azealiaa/flask_project/G2_PROJECT/static/images/" + user + "_" + image_name[0] + ".png"
            image_path = "/static/images/" + user + "_" + image_name[0] + ".png"
            audio_path = "/static/music/" + user + "_" + filename
            file = "/home/azealiaa/flask_project/G2_PROJECT/static/music/" + user + "_" + filename 
            plt.clf()
            signal, sr = librosa.load(file)
            plt.figure(figsize=(10,10))
            plt.subplot(211)
            librosa.display.waveplot(signal,sr)
            plt.title('Waveform and Spectogram') # waveform of %r % file for title
            plt.ylabel("Amplitude")
            X = librosa.stft(signal)
            Xdb = librosa.amplitude_to_db(abs(X))
            plt.subplot(212)
            librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
            plt.show()
            plt.savefig(image)
            
            duration = librosa.get_duration(y=signal,sr=sr)
            file_size_byte = os.path.getsize(file)
            file_size = file_size_byte/1024
            
            new_sound = Sounds( data=audio.read(), title=filename, username=request.form["username"], location=request.form["location"], sound_path=audio_path, waveform_path=image_path, file_type=image_name[1], file_duration=duration, file_size=file_size, sampling_freq=sr)
            
            try:
                db.session.add(new_sound)
                db.session.commit()
                return redirect ('/confirm')

            except:
                return "There was an error"

    else:
        return render_template("upload.html")

@app.route("/record", methods=['POST', 'GET'])
def record():
    db.create_all()

    if request.method == "POST":
        f = open('./file.wav', 'wb')
        f.write(request.get_data("audio_data"))
        f.close()
        if os.path.isfile('./file.wav'):
            print("./file.wav exists")

        return render_template('record.html', request="POST")   
    else:
        return render_template("record.html")

app.config["FILE_UPLOADS"] = "/home/azealiaa/flask_project/G2_PROJECT/static/music"

if __name__ == "__main__":
    app.run(debug=True)
