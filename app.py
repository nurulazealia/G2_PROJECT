from flask import Flask, render_template, redirect, request, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tables import Results
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Sounds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
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

@app.route("/lists")
def lists():
    sounds = Sounds.query.order_by(Sounds.date_uploaded)
    return render_template("lists.html", sounds=sounds)

@app.route("/delete/<int:id>")
def delete(id):
    list_to_delete = Sounds.query.get_or_404(id)
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
    

@app.route("/database", methods = ['POST', 'GET'])
def database():
    db.create_all()
    
    if request.method == "POST":
        file = request.files['inputFile']
        new_sound = Sounds(title=file.filename, data=file.read())

        try:
            db.session.add(new_sound)
            db.session.commit()
            return redirect ('/database')

        except:
            return "There was an error"

    else:
        sounds = Sounds.query.order_by(Sounds.date_uploaded)
        table = Results(sounds)
        table.border = True
        return render_template("database.html", sounds=sounds, table=table)

if __name__ == "__main__":
    app.run(debug=True)