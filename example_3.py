from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template(
        'user.html',
        name='Subat',
        time=datetime.now()
    )