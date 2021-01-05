from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///127.0.0.1:5000/database'

db = SQLAlchemy(app)

class Sounds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Title %r>' %self.id

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/lists", methods = ['POST', 'GET'])
def lists():
    db.create_all()
    
    if request.method == "POST":
        sound_title = request.form['title']
        new_sound = Sounds(title=sound_title)

        try:
            db.session.add(new_sound)
            db.session.commit()
            return redirect ('/lists')

        except:
            return "There was an error"

    else:
        sounds = Sounds.query.order_by(Sounds.date_uploaded)
        return render_template("lists.html", sounds=sounds)

if __name__ == "__main__":
    app.run(debug=True)