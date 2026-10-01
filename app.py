from flask import Flask, flash, render_template, session, redirect, url_for, request
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

class ChatForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'name' in session and 'email' in session:
        return redirect('/chat')
    
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        if 'utoronto' not in email.lower():
            flash('Please enter a UofT email address.', 'danger')
        else:
            session['name'] = name
            session['email'] = email

            return redirect(('/chat'))

    return render_template(
        'user.html',
        form=form
    )


@app.route("/chat", methods=["GET", "POST"], endpoint="chatPage")
def chat():
    if 'name' not in session or 'email' not in session:
        return redirect('/')
    form = ChatForm()
    
    if form.validate_on_submit():
        message = form.message.data
        message_lower = message.lower()

        if message_lower.startswith("my name is "):
            name = message[len("my name is "):].strip()

            if name.endswith("."):
                name = name[:-1].strip()

            session["data_name"] = name
            reply = f"Nice to meet you, {name}!"

        elif "what is my name" in message_lower:
            name = session.get("data_name")

            if name:
                reply = f"Your name is {name}."
            else:
                reply = "I don't know."

        elif "hello" in message_lower:
            reply = "Hello!"
        else:
            reply = "I don't understand."

        messages = session.get("messages", [])

        messages.append({
            "message": message,
            "reply": reply
        })

        session["messages"] = messages

    messages = session.get("messages", [])

    return render_template(
        "chat.html",
        form=form,
        messages=messages
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')