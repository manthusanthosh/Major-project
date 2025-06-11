from flask import Flask,render_template,redirect,url_for,request
import numpy as np
import pandas as pd
import mysql.connector,joblib

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3307",
    database='cellular_traffic'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT UPPER(email) FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered! Please go to login section")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                global user_email
                user_email = email

                return redirect("/home")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')
    

@app.route('/prediction',methods=['POST','GET'])
def prediction():
    if request.method == 'POST':
       User_Throughput_Mbs = int(request.form['User_Throughput_Mbs'])
       Cell_Throughput_Mbs = int(request.form['Cell_Throughput_Mbs'])
       Radio_Bearers_Traffic_GB = int(request.form['Radio_Bearers_Traffic_GB'])
       Downlink_Traffic_Volume_GB = int(request.form['Downlink_Traffic_Volume_GB'])
       Uplink_Traffic_Volume_GB = int(request.form['Uplink_Traffic_Volume_GB'])
       Signal_Quality_SIR = int(request.form['Signal_Quality_SIR'])
       Day_of_Week = int(request.form['Day_of_Week'])
       Network_Type_4G5 = int(request.form['Network_Type_4G5'])
       Month = int(request.form['Month'])
       Hour = int(request.form['Hour'])

       # Load the saved models
       rf_model = joblib.load('linear.joblib')
       input_data = np.array([[User_Throughput_Mbs,Cell_Throughput_Mbs, Radio_Bearers_Traffic_GB,Downlink_Traffic_Volume_GB, Uplink_Traffic_Volume_GB,Signal_Quality_SIR, Day_of_Week,Network_Type_4G5, Month, Hour]])

        # Make predictions using the loaded models
       rf_prediction = rf_model.predict(input_data)

        # Display the predictions
       msg = rf_prediction[0]
       return render_template('prediction.html',msg = msg)
    return render_template('prediction.html')
    


if __name__ == '__main__':
    app.run(debug = True)