from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from tools import DB
import os
import threading
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

tv_db = DB("data")

@app.route('/')
def index():
    genres = ['Comedy', 'Drama', 'Action', 'Science-Fiction']
    shows_by_genre = {}
    for genre in genres:
        df = tv_db.query("SELECT * FROM shows WHERE genre_tag = :g LIMIT 6", {"g": genre})
        shows_by_genre[genre] = df.to_dict(orient='records')
    return render_template("index.html", shows_by_genre=shows_by_genre)

@app.route('/show/<int:show_id>')
def show_detail(show_id):
    df = tv_db.query("SELECT * FROM shows WHERE id = :id", {"id": show_id})
    if df.empty:
        return "Show not found", 404
    show = df.iloc[0].to_dict()
    return render_template("show.html", show=show)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    results = []
    if q:
        df = tv_db.query("SELECT * FROM shows WHERE name LIKE :q", {"q": f"%{q}%"})
        results = df.to_dict(orient='records')
    return render_template("index.html", shows_by_genre={"Search Results": results})

# Auto-open browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)

