from email.headerregistry import UniqueSingleAddressHeader
from flask import Flask, render_template, request, redirect,session, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import joblib
import pandas as pd
# import numpy as np


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    # atribut class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), Unique=True)
    password = db.COlumn(db.String(100))
    
    # fungsi init memasukkan username dan password
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run()

#                    End Of Login Form SQL ~ Flask
# ---------------------------------------------------------------------- # 

@app.route('/', methods=['GET','POST'])
def main():
    return render_template('index.html')

@app.route('/masterpeta', methods=['GET','POST']) 
def masterpeta():
    if request.method == 'GET':
        print(request.form)
        return render_template('masterpeta.html')
    if request.method == 'POST':
        return render_template('masterpeta.html',menu='master', submenu='peta')


@app.route('/masterprediksi', methods=['GET','POST']) 
def masterprediksi():
    if request.method == 'GET':
        print(request.form)
        return render_template('masterprediksi.html')
    elif request.method == 'POST':
         # Get values through input bars
        model  = joblib.load("model_development/model_predict_home_price.pkl")
        income = request.form.get("income")
        age = request.form.get("age")
        if float(age) < 2.6:
            age = str(2.6)
        bathroom = request.form.get("bathroom")
        if int(bathroom) < 3:
            bathroom =  str(3)
        bedroom = request.form.get("bedroom")
        if int(bedroom) < 2:
            bedroom = str(2)
        population = request.form.get("population")
        
        # Put inputs to dataframe
        X = pd.DataFrame([[income, age, bathroom, bedroom, population]], columns = ["income", "age", "bathroom", "bedroom", "population"])
     
        # Get prediction
        predict_price = round(model.predict(X)[0],2)      
    else:
        predict_price = ""    
    return render_template("masterprediksi.html", output = predict_price)


@app.route('/masterprediksiusia', methods=['GET','POST']) 
def masterprediksiusia():
    if request.method == 'GET':
        print(request.form)
        return render_template('masterprediksiusia.html')
    elif request.method == 'POST':
         # Get values through input bars
        model2 = joblib.load("model_development/model_predict_home_age.pkl")
        income = request.form.get("income")
        bathroom = request.form.get("bathroom")
        if int(bathroom) < 3:
            bathroom =  str(3)
        bedroom = request.form.get("bedroom")
        if int(bedroom) < 2:
            bedroom = str(2)
        population = request.form.get("population")
        price = request.form.get("price")
        
        # Put inputs to dataframe
        X = pd.DataFrame([[income, bathroom, bedroom, population, price]], columns = ["income", "bathroom", "bedroom", "population", "price"])
        
        # Get prediction
        predict_age = round(model2.predict(X)[0])      
    else:
        predict_age = ""   
    return render_template("masterprediksiusia.html", output_age = predict_age)


if __name__ == "__main__":
    app.run()