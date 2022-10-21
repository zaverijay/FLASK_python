from flask import Flask, render_template, redirect, url_for, request
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'

db = SQLAlchemy(app)

class CRUD(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(12))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def index():
    all_data = CRUD.query.all()
    return render_template('index.html', employees=all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = CRUD(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':

        my_data = CRUD.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = CRUD.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)