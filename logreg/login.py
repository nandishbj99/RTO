from flask import *
from wtforms import Form,StringField,SelectField,PasswordField,validators,SubmitField,TextField,IntegerField,BooleanField
import sqlite3,hashlib,os
from flask import request
import os
import pdfkit
from datetime import date,timedelta
from flask_wtf.file import FileField, FileRequired

from flask_pymongo import PyMongo
app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/rto"
mongo = PyMongo(app)

#::::::::::::::::::::::::::::::::::::::::class::::::::::::::::::::::::::


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
    fathersname=StringField('fathersname',[validators.Length(min=3,max=10)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    address=TextField('caddress',[validators.DataRequired()])
    pincode=IntegerField('pincode')
    city=StringField('City',[validators.DataRequired()])
    district=StringField('District',[validators.DataRequired()])
    state=StringField('State',[validators.DataRequired()])
    country=StringField('Country',[validators.DataRequired()])
    dob=StringField('DOB',[validators.DataRequired(),validators.Length(min=10,max=10)])
    age=IntegerField('age')
    gender=SelectField('gender',choices=[('male','male'),('female','female')])
    phone=IntegerField('Phone')
    blood_group=StringField('Blood_Group',[validators.DataRequired()])
    typee=SelectField('typee',choices=[('lmv','lmv'),('mcwg','mcwg')])
    

#validating the login fields
class mylogform(Form):
    email=TextField('email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('password',[validators.DataRequired()])
app.secret_key='nandish'

#:::::::::::::::::::::::::::::::::entry main pages::::::::::::::::::::::::::::::::::::::
#home page
@app.route('/')
def home():
    
    return render_template('home.html')


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


@app.route('/logout/')
def logout():
    session.pop('logname', None)
    session.pop('email', None)
    return(redirect(url_for('home')))

#:::::::::::::::::::::::::::::::::::::::::::::users pages::::::::::::::::::::::::::::
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



#form to pdfconverter
@app.route('/formtopdf',methods=['POST','GET'])
def formtopdf():
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            email=session.get('email')
            cur.execute("SELECT * FROM llr WHERE email=?",(email,))
            data=cur.fetchone()       
    rendered=render_template("llrform.html",data=data)
    pdf=pdfkit.from_string(rendered,False)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='attachment; filename=llr.pdf' #downloadable file 
    return response
        

@app.route("/llr",methods=["GET","POST"])
def llrapply():
    form=llr_user(request.form)
    if request.method == 'POST' and form.validate():
        firstname=form.firstname.data
        lastname=form.lastname.data
        fathersname=form.fathersname.data
        email=form.email.data
        address=form.address.data
        pincode=form.pincode.data
        city=form.city.data
        district=form.district.data
        state=form.state.data
        country=form.country.data
        dob=form.dob.data
        age=form.age.data
        gender=form.gender.data
        phone=form.phone.data
        bloodgroup=form.blood_group.data
        currentdate= date.today()
        expirydate = date.today()+timedelta(30)
        typee=form.typee.data

        #files_
        
        aadharpdf= request.files["aadhar"]  
        sslcpdf = request.files["sslc"]
        voteridpdf = request.files["voterid"]
        photo= request.files["photo"]
        signature= request.files["signature"]
        status="pending"
        with sqlite3.connect('r.db') as con:
            try:
                cur=con.cursor()
                cur.execute("INSERT INTO llr (firstname,lastname,fathername,email,address,pincode,city,district,state,country,dob,age,gender,phone,bloodgroup,currentdate,expirydate,status,type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(firstname,lastname,fathersname,email,address,pincode,city,district,state,country,dob,age,gender,phone,bloodgroup,currentdate,expirydate,status,typee))
                con.commit()
                flash("reg successfully")
                try:
                    mongo.save_file(aadharpdf.filename,aadharpdf)
                    mongo.save_file(sslcpdf.filename,sslcpdf)
                    mongo.save_file(voteridpdf.filename,voteridpdf)
                    mongo.save_file(signature.filename,signature)
                    mongo.save_file(photo.filename,photo)
                    mongo.db.users.insert({'email':email,'aadharpdf':aadharpdf.filename,'sslcpdf':sslcpdf.filename,'voterid':voteridpdf.filename,'signature':signature.filename,'photo':photo.filename})
                except:
                    print("mongo error")
            except:
                con.rollback()
                flash("error occur")
        con.close()
                
        return redirect(url_for('success'))
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
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT status FROM llr WHERE email = ?",(session.get('email'),))
            st=cur.fetchone()
            if st[0] == "pending":
                return render_template("statuspending.html") 
            elif st[0] == "declined":
                return render_template("statusdeclined.html")
            else:
                return render_template("statusaccepted.html")
            con.close()
    

@app.route('/success')
def success():
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            email=session.get('email')
            cur.execute("SELECT * FROM llr WHERE email=?",(email,))
            data=cur.fetchone()
            ren=render_template("llrform.html",data=data)       
    
    return ren

#USERDASHBOARD
@app.route('/userdashboard')
def userdash():
    return render_template("userdashboard.html")







#:::::::::::::::::::::::::::::::::::::::::::employee:::::::::::::::::::::::::::::::::::::::::
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



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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



    

    
"""form=uploadllr(request.form)
        print("booo")
        if request.method=='POST' and form.validate(): #NOT GOING....
        print("YOO")  #FIX THIS
        llrdb(name="n",file1=form.file1.data.read(),file2=form.file2.data.read(),file3=form.file3.data.read())
        print("ERROR !")
        return "Request Submitted
    return render_template("applyllr.html")"""
if(__name__=="__main__"):
    app.run(debug=True)

