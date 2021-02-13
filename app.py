from flask import Flask, render_template, redirect, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tables import Results, Explore
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Sounds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    data = db.Column(db.LargeBinary)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Title %r>' %self.id



@app.route("/", methods = ['GET'])
def home():
    #file_data = Sounds.query.filter_by(id=1).first()
    playlist = os.listdir('static/music/')
    return render_template("home.html", playlist=playlist)
    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/explore")
def explore():
    sounds = Sounds.query.order_by(Sounds.date_uploaded)
    table1 = Explore(sounds)
    return render_template("explore.html", sounds=sounds, table1=table1)

@app.route("/show/<int:id>", methods = ['GET'])
def show(id):
    list_to_show = Sounds.query.get_or_404(id)
    playing = list_to_show.title
    playlist = "/static/music"+playing
    return render_template("show.html", list_to_show = list_to_show, playing=playing, playlist=playlist)

@app.route("/delete/<int:id>")
def delete(id):
    list_to_delete = Sounds.query.get_or_404(id)
    filename = list_to_delete.title
    os.remove(os.path.join(app.config["FILE_UPLOADS"], filename))
    try:
        db.session.delete(list_to_delete)
        db.session.commit()
        return redirect('/database')
    except:
        return "There was a problem deleting"

@app.route("/update/<int:id>", methods = ['POST', 'GET'])
def update(id):
    list_to_update = Sounds.query.get_or_404(id)
    if request.method == "POST":
        list_to_update.title = request.form['title']
        try:
            db.session.commit()
            return redirect('/database')
        except:
            return "There was a problem updating the database"
    else:
        return render_template("update.html", list_to_update = list_to_update)
    
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

    return render_template("database.html", sounds=sounds, table=table)

@app.route("/confirm")
def confirm():
    
    return render_template("confirm.html")

app.config["FILE_UPLOADS"] = "/home/azealiaa/flask_project/G2_PROJECT/static/music"

@app.route("/upload", methods = ['POST', 'GET'])
def upload():
    db.create_all()
    
    if request.method == "POST":

        if request.files:

            audio = request.files['inputFile']
            filename = secure_filename(audio.filename)
            audio.save(os.path.join(app.config["FILE_UPLOADS"], filename))

            new_sound = Sounds( data=audio.read(), title=filename, username=request.form["username"], location=request.form["location"])
            try:
                db.session.add(new_sound)
                db.session.commit()
                return redirect ('/confirm')

            except:
                return "There was an error"

    else:
        return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)