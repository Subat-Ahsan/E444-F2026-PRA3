from flask import Flask, flash, render_template, session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from datetime import datetime

from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adsfasdfws'
Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField("What is your Name?", validators=[DataRequired()])
    email = EmailField("What is your UofT Email?")
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        if 'utoronto' not in email.lower():
            flash('Please enter a UofT email address.', 'danger')
        else:
            previous_name = session.get('name')
            previous_email = session.get('email')

            if previous_name is not None and previous_name != name:
                flash("Looks like you changed your name.")

            if previous_email is not None and previous_email != email:
                flash("Looks like you changed your email.")

            session['name'] = name
            session['email'] = email

            return render_template(
                'user.html',
                name=name,
                email=email,
                time=datetime.now(),
                form=form
            )

    return render_template(
        'user.html',
        form=form
    )