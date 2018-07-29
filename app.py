import datetime
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "First Code Academy"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FirstCodeSecrets.db'
db = SQLAlchemy(app)

class Secrets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    flag = db.Column(db.Integer, nullable=False)

    def __init__(self, title, content, flag):
        self.title = title
        self.content = content
        self.flag = flag

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content']:
            flash('Please enter all the fields', 'error')
        else:
            title = request.form['title']
            content = request.form['content']
            flag = 0

            secret = Secrets(title=title, content=content, flag=flag)
            db.session.add(secret)
            db.session.commit()

    return render_template('add.html')


@app.route('/main')
def wall():
    return render_template('wall.html', secrets=Secrets.query.all())


@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        if not request.form['id'] or not request.form['reason']:
            flash('Please enter all the fields', 'error')
        else:
            id = request.form['id']
            secret = Secrets.query.filter_by(id=id).first()
            secret.flag += 1

            db.session.commit()
            flash('Report has been sent to the administrator.')
            return redirect(url_for('wall'))

    return render_template('report.html')


if __name__ == '__main__':
    app.run()
