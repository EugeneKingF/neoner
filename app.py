from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import forms
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "a6ed9e81e4ea3c71431caef6cef8f21a"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.sqlite3'

db = SQLAlchemy(app)
base_url = "http://neoner.cc/"


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_link = db.Column(db.String)
    full_link = db.Column(db.String)


def random_link():
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(6))


@app.route('/', methods=["GET", "POST"])
def index():
    result = ''
    short_link_create = ''
    form = forms.LinkForm()
    if request.method == "POST":
        link = form.link.data
        if link is None:
            result = "Input is empty"
        elif link[0:8] != "https://" or link[0:7] != "http://":
            result = "The link isn't correct"
        else:
            short_link_create = base_url + random_link()
        while Link.query.filter_by(short_link=short_link_create).first() is not None:
            short_link_create = base_url + random_link()
        saver = Link(short_link=short_link_create, full_link=link)
        db.session.add(saver)
        db.session.commit()
    return render_template('index.html', form=form, result=short_link_create)


@app.route('/<option_link>')
def short_to_ling(option_link):
    if option_link == 'contact':
        return render_template('contact.html')
    elif option_link == 'privacy-policy':
        return render_template('privacy-policy.html')
    else:
        full_short_link = base_url + option_link
        link = Link.query.filter_by(short_link=full_short_link).first()
        return redirect(link.full_link)


if __name__ == '__main__':
    app.run()
