from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

server = Flask(__name__)


server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)


class Urls(db.Model):
    id = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(5))

    def __init__(self, long, short):
        self.long = long
        self.short = short

    def __str__(self):
        return f'Long URL:{self.long}, short URL:{self.short}'


@server.before_first_request
def create_tables():
    db.create_all()


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=5)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters


@server.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        url_recieved = request.form["url"]
        # check if url is in db
        found_url = Urls.query.filter_by(long=url_recieved).first()
        if found_url:
            # return short url if found
            # return found_url.short
            return redirect(url_for("display_short_url", url=found_url.short))

        else:
            short_url = shorten_url()
            new_url = Urls(url_recieved, short_url)
            db.session.add(new_url)
            db.session.commit()
            # return short_url
            return redirect(url_for("display_short_url", url=short_url))

            # long_URL = request.form['url']
    else:
        return render_template("index.html")


@server.route('/display/<url>')
def display_short_url(url):
    return render_template("shorturl.html", short_url_display=url)


@server.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    server.run(debug=True)
