from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class LinkForm(FlaskForm):
    link = StringField('Full link', render_kw={"placeholder": "Example: https://example.com or http://example.com"})
    submit = SubmitField('Create short link')