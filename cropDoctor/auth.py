from flask import Blueprint , render_template , request , jsonify, redirect, url_for
from .db import collection
from .import model as m
from werkzeug.utils import secure_filename
import os
import wikipedia

auth=Blueprint("auth",__name__)

@auth.route("/login" , methods=['GET','POST'])  
def login():
    emailid=request.form.get("login-email")
    password1=request.form.get("login-password")
    return render_template("login.html")

@auth.route("/register" , methods=['GET','POST'])
def register():
    if request.method == "POST":
        emailid=request.form.get("email")
        p1 = collection.find_one({"Email": emailid})
        if(p1!=None):
            message = 'Credentials already Exists'
            return render_template('register.html', message=message)
        name=request.form.get("name")
        password1=request.form.get("password1")
        password2=request.form.get("password2")
        if password1 != password2:
                message = 'Passwords should match!'
                return render_template('register.html', message=message)
        else:
            user_input = {'Name': name, 'Email': emailid ,'Password':password1}
            print(user_input)
            collection.insert_one(user_input)
            message = 'Please login using your credentials'
            return render_template("login.html",message = message)
    return render_template("register.html")

@auth.route('/verifylogin',methods=['POST'])  # type: ignore
def logged_in():
    if request.method == "POST":
        EmailId = request.form.get("login-email")
        Password = request.form.get("login-password")
        p1 = collection.find_one({"Email": EmailId})
        if(p1==None):
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        if Password==p1["Password"]:
            p2=collection.find_one({"Email": EmailId},{'_id':0,'Email':0,'Password':0})
            p2=dict(p2)  # type: ignore
            print(p2)
            Name=p2['Name']
            return render_template("home.html",message=Name)
        else:
            error = 'Wrong Password!!'
            return render_template('login.html',error=error)

@auth.route('/predict',methods= ['GET','POST']) #type: ignore
def pred():
    msg = ""
    f = request.files['file']
    basepath = '/Users/rishipv/CropDoctor/CropDoctor-main'
    file_path = os.path.join(basepath, 'uploads',secure_filename(f.filename))#type:ignore
    f.save(file_path)
    res = m.myModel.predict([m.prepare(file_path)] )#type:ignore
    import numpy as np
    classresult=np.argmax(res,axis=1)
    msg=m.classes[classresult[0]]
    msg = msg.replace('__',' ').replace('_',' ')
    result = wikipedia.summary(msg, sentences=2)
    url = wikipedia.page(result).url
    return render_template("pred_res.html",message = msg,result = result,url = url)


@auth.route("/home" , methods=['GET','POST'])
def home():
    return render_template("home.html")

