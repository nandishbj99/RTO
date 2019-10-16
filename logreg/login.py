from flask import *
from wtforms import Form,StringField,SelectField,PasswordField,validators,SubmitField,TextField,IntegerField,BooleanField
import sqlite3,hashlib,os
from flask import request
import os
import pdfkit
from flask_wtf.file import FileField, FileRequired
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/rto"
mongo = PyMongo(app)



#togetlogin details:
"""
def getlogindetails():
    with sqlite3.connect('r.db') as conn:
        cur=conn.cursor()
        if 'email' not in session:
            loggedIn=False
            loggeduname=""
        else:
            loggedIn=True
            
            cur.execute("SELECT firstname,lastname FROM users WHERE email= ?",(session['email'],))
            fname,lname=cur.fetchone()

            loggeduname=fname+""+lname
    conn.close()
    return (loggedIn, loggeduname)"""



#validating the register fields
class myform(Form):
    firstname=StringField('Firstname',[validators.Length(min=3,max=12)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('NewPassword',[validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm=PasswordField('confirmPassword')
    lastname=StringField('Lastname',[validators.Length(min=1,max=10)])
    phone=IntegerField("Phone")

#validating the LLR_user deatils
class llr_user(Form):
    firstname=StringField('Firstname',[validators.Length(min=3,max=12)])
    lastname=StringField('Lastname',[validators.Length(min=3,max=10)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    caddress=TextField('caddress',[validators.DataRequired()])
    pincode=IntegerField('pincode',[validators.Length(min=6,max=6)])
    district=StringField('District',[validators.DataRequired()])
    state=StringField('State',[validators.DataRequired()])
    dob=StringField('DOB',[validators.DataRequired(),validators.Length(min=10,max=10)])
    gender=SelectField('gender',choices=[('male','male'),('female','female')])
    phone=IntegerField('Phone')
    blood_group=StringField('Blood_Group',[validators.DataRequired()])
    

#validating the login fields
class mylogform(Form):
    email=TextField('email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('password',[validators.DataRequired()])
app.secret_key='nandish'



#about page
@app.route('/about')
def about():
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT email,password,firstname,lastname FROM users")
            data=cur.fetchall()
            return render_template('about.html',data=data[1][0])


#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#register page
@app.route('/register',methods=['POST','GET'])
def reg():
    form=myform(request.form)
    if request.method=='POST' and form.validate():
        fname=form.firstname.data
        lname=form.lastname.data
        phone=form.phone.data
        password=form.password.data
        email=form.email.data
        with sqlite3.connect('r.db') as con:
            try:
                cur=con.cursor()
                cur.execute("INSERT INTO users (email,password,firstname,lastname,phone) VALUES (?,?,?,?,?)",(email,hashlib.md5(password.encode()).hexdigest(),fname,lname,phone))
                con.commit()
                flash("reg successfully")
            except:
                con.rollback()
                flash("error occur")
        con.close()
        return redirect(url_for('home'))
    else:
        return render_template('reg.html',form=form)

#home page
@app.route('/')
def home():
    
    return render_template('home.html')


#login page
@app.route('/login',methods=['POST','GET'])
def login():
    form=mylogform(request.form)
    if request.method=='POST' and form.validate():
        useremail=form.email.data
        upassword=form.password.data
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            if(cur.execute("SELECT email,password,firstname,lastname FROM users WHERE email=? and password=?",(useremail,hashlib.md5(upassword.encode()).hexdigest()))):
                data=cur.fetchone()
                session['email']=useremail
                session['logname']=data[2]

                flash('Loged in','success')
                return redirect(url_for('userdash'))
            else:
                flash("please register first and login")
                return redirect(url_for('home'))
                

    return render_template("login_page.html",form=form)



#dlr page
@app.route('/dlr')
def dlr():
    return render_template("applydlr.html")


#class uploadSSLC(Form):
 #   file = FileField()
 #   submit = SubmitField("Submit")
#class uploadADHAR(Form):
  ##  file = FileField()
    #submit = SubmitField("Submit")
'''class uploadllr(Form):
    file1 = FileField(validators=[FileRequired()])
    submit = SubmitField("Submit")
    file2 = FileField(validators=[FileRequired()])
    submit2 = SubmitField("Submit")
    file3 = FileField(validators=[FileRequired()])
    submit3 = SubmitField("Submit")
    check = BooleanField("Consent")'''


"""def llrdb(name,file1,file2,file3):
        with sqlite3.connect('r.db') as con:
        cursor=con.cursor()
        #cursor.execute("" CREATE table llr(uname TEXT,file1 BLOB,file2 BLOB,file3 BLOB)"")
        try:
            cursor.execute(" INSERT INTO llr(uname,file1,file2,file3) VALUES(?,?,?,?)",(name,file1,file2,file3))
        except:
            print("ERROR")
        con.commit()
        cursor.close()"""




    

    
"""form=uploadllr(request.form)
        print("booo")
        if request.method=='POST' and form.validate(): #NOT GOING....
        print("YOO")  #FIX THIS
        llrdb(name="n",file1=form.file1.data.read(),file2=form.file2.data.read(),file3=form.file3.data.read())
        print("ERROR !")
        return "Request Submitted
    return render_template("applyllr.html")"""

#form to pdfconverter
@app.route('/formtopdf',methods=['POST','GET'])
def formtopdf():
    rendered=render_template("contact.html")
    pdf=pdfkit.from_string(rendered,False)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=output.pdf'
    response.headers['Content-Disposition']='attachment; filename=output.pdf' #downloadable file


    
    return response
        
        


"""def llrdb(file):
    with sqlite3.connect('r.db') as con:
        cursor=con.cursor()
        try:
            cursor.execute(" CREATE table IF NOT EXISTS sample(data BLOB)")
        except:
            print("ERROR1")
        try:
            cursor.execute(" INSERT INTO sample(data) VALUES(?)",(file))
        except:
            print("ERROR2")
        con.commit()
        cursor.close()"""


"""def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData"""

@app.route("/llr",methods=["GET","POST"])
def llrapply():
    form=llr_user(request.form)
    if request.method == 'POST':
        
        firstname=form.firstname.data
        lastname=form.lastname.data
        email=form.email.data
        caddress=form.caddress.data
        paddress=form.paddress.data
        pincode=form.pincode.data
        district=form.district.data
        state=form.state.data
        dob=form.dob.data
        gender=form.gender.data
        eduqal=form.edu_qal.data
        phone=form.phone.data
        bloodgroup=form.blood_group.data
        filee= request.files["uploadfile"]#files
        mongo.save_file(filee.filename,filee)
        username=request.form['username']
        mongo.db.users.insert({'username':username,'filename':filee.filename})
        render_template("submitted.html")
    else:
        return render_template("appllr.html",form=form)


        
            
        
            
            



    

#toshow pdff files
@app.route('/showpdf',methods=['GET','POST'])
def showpdf():
    if request.method=='POST':
        username=request.form['username']
        user=mongo.db.users.find_one({'username':username})
        filename=user['filename']
        return mongo.send_file(filename)
    return render_template("showpdf.html")



@app.route('/regv')
def regv():
    return render_template("regv.html")

@app.route('/status')
def status():
    return render_template("reqstatus.html")

#USERDASHBOARD
@app.route('/userdashboard')
def userdash():
    return render_template("userdashboard.html")

@app.route('/empdashboard')
def empdash():
    return render_template("empdashboard.html")

@app.route('/emplogin',methods=['POST','GET'])
def emplogin():
    form=mylogform(request.form)
    if request.method=='POST' and form.validate():
        empemail=form.email.data
        emppassword=form.password.data
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            if(cur.execute("SELECT email,password FROM admin WHERE email=? and password=?",(empemail,emppassword))):
                flash('Logged in','success')
                return redirect(url_for('empdash'))
            else:
                flash("please contact admin for registration")
                return redirect(url_for('home'))
                

    return render_template("emplogin.html",form=form)

@app.route('/logout/')
def logout():
    session.pop('logname', None)
    session.pop('email', None)
    return(redirect(url_for('home')))
if(__name__=="__main__"):
    app.run(debug=True)
