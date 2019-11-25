from flask import *
from wtforms import Form,StringField,SelectField,PasswordField,validators,SubmitField,TextField,IntegerField,BooleanField
import sqlite3,hashlib,os
from flask import request
import os
import smtplib 
from email.mime.text import MIMEText
import pdfkit
from datetime import date,timedelta,datetime
from flask_wtf.file import FileField, FileRequired
import random
import math, random 
import io
import base64


from flask_pymongo import PyMongo
app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/rto"
mongo = PyMongo(app)

#::::::::::::::::::::::::::::::::::::::::class::::::::::::::::::::::::::::::::::::::::::::::::

class ChoicesByDb(object):
    def __iter__(self):
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM rtocodes")
            data=cur.fetchall()
        for row in data:
            pair = (row[1],row[1]+" "+row[2])
            yield pair

#validating the register fields
class myform(Form):
    firstname=StringField('Firstname',[validators.Length(min=3,max=12)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('NewPassword',[validators.DataRequired(),validators.EqualTo('confirm', message='Password Is Not Matching')])
    confirm=PasswordField('Confirm Password')
    lastname=StringField('Lastname',[validators.Length(min=1,max=10)])
    phone=TextField("Phone",[validators.Length(min=1,max=10)])
    otp=IntegerField("Enter OTP")

#validating the LLR_user deatils
class llr_user(Form):
    firstname=StringField('Firstname',[validators.Length(min=3,max=12)])
    lastname=StringField('Lastname',[validators.Length(min=3,max=10)])
    fathersname=StringField('Fathers Name',[validators.Length(min=3,max=10)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    address=TextField('Address',[validators.DataRequired()])
    pincode=IntegerField('Pincode')
    city=StringField('City',[validators.DataRequired()])
    district=StringField('District',[validators.DataRequired()])
    state=StringField('State',[validators.DataRequired()])
    country=StringField('Country',[validators.DataRequired()])
    """dob=StringField('Date Of Birth',[validators.DataRequired(),validators.Length(min=10,max=10)])
    age=IntegerField('Age')"""
    gender=SelectField('Gender',choices=[('male','male'),('female','female')])
    phone=IntegerField('Phone')
    blood_group=StringField('Blood Group',[validators.DataRequired()])
    rtooffice=SelectField(choices=ChoicesByDb(),label="RTO Office")
    
class regvehi(Form):
    firstname=StringField('Firstname',[validators.Length(min=3,max=12)])
    lastname=StringField('Lastname',[validators.Length(min=3,max=10)])
    fathersname=StringField('fathersname',[validators.Length(min=3,max=10)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    address=TextField('Address',[validators.DataRequired()])
    enginenumber=StringField('Engine Number',[validators.Length(min=10,max=10)])
    ownership=SelectField('Ownership',choices=[('1','INDIVIDUAL'),('2','MULTIPLE OWNER'),('3','CORPORATION')])
    vetype = SelectField('Vehicle type',choices=[('transport','TRANSPORT'),('nontransport','NON TRANSPORT')])
    vclass = SelectField('Vehicle class',choices=[('car','CAR'),('bike','M-CYCLE'),('scooty','M-SCOOTER'),('bus','OB-BUS'),('truck','TWITPKV-TRUCK')])
    purchasedate = StringField('Purchasedate')
    manufacture = StringField('Manufacturer')
    modelname = StringField('Model Name')
    manufacturedate = StringField('Manufacturedate')
    fuel = SelectField('Fuel',choices = [('petrol','PETROL'),('diesel','DIESEL'),('lpg','LPG / DIE'),('electric','ELECTRIC'),('solor','SOLOR')])
    color = StringField('Color')
    insurencecompany = StringField('Insurance Company')
    datefrom = StringField('Valid From')
    dateto = StringField('Valid Till')
    insurancenumber = StringField('Cover Number', [validators.Length(min=10,max=10)])


class passwordform(Form):
    old=PasswordField('OLD password',[validators.DataRequired()])
    password=PasswordField('NEW password',[validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm=PasswordField('Confirm Password')
class mylogform(Form):
    email=TextField('Email',[validators.Email(),validators.DataRequired()],render_kw={"placeholder": "Email"})
    password=PasswordField('Password',[validators.DataRequired()],render_kw={"placeholder": "Password"})
    
app.secret_key='nandish'
class emplogform(Form):
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('Password',[validators.DataRequired()])
    secretkey=PasswordField('Secret Key',[validators.DataRequired()])
class vrdl(Form):
    enginenumber=TextField('Engine Number',[validators.Length(min=10,max=10)])
    
class adstatus(Form):
    date = TextField('date')

#:::::::::::::::::::::::::::::::::entry main pages::::::::::::::::::::::::::::::::::::::
#home page

"""def mail(email,message):
    msg=MIMEText(message)
    msg['From']="karnatakartostatus@gmail.com"
    msg['To']=email
    msg['Subject']="RTO UPDATE"
    SERVER=smtplib.SMTP('smtp.gmail.com',587)
    SERVER.starttls()
    SERVER.login("karnatakartostatus@gmail.com","lenovoasus")
    SERVER.send_message(msg)
    SERVER.quit()"""


def mail(email,message):
    smtp_ssl_host = 'smtp.mail.yahoo.com'
    smtp_ssl_port = 465
    username = 'karnatakartostatus@yahoo.com'
    password = 'vnty ojfh flkc ctqp'
    sender = 'karnatakartostatus@yahoo.com'
    targets = email

    msg = MIMEText(message)
    msg['Subject'] = 'RTO Update'
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()


  
def generateOTP() :
    return random. randrange(1000, 9999, 20)





@app.route('/')
def home():
    return render_template('home.html')


#about page
@app.route('/about')
def about():
        return render_template('about.html')

@app.route('/polc')
def pol():
        return render_template('pollcontrol.html')

@app.route('/safety')
def safe():
        return render_template('roadsafety.html')
        
@app.route('/act')
def act():
        return render_template('actsrules.html')

#contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/logout/')
def logout():
    session.pop('logname', None)
    session.pop('email', None)
    session.pop('key',None)
    return(redirect(url_for('home')))








#:::::::::::::::::::::::::::::::::::::::::::::users pages:::::::::::::::::::::::::::::::


        
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::;login page
@app.route('/login',methods=['POST','GET'])
def login():
    form=mylogform(request.form)
    if request.method=='POST' and form.validate():
        useremail=form.email.data
        upassword=form.password.data
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            try:
                cur.execute("SELECT email,password,firstname,lastname FROM users WHERE email=? and password=?",(useremail,hashlib.md5(upassword.encode()).hexdigest()))
                data=cur.fetchone()
                if data:
                    session['email']=useremail
                    session['logname']=data[2]
                    session['key']="user"
                    flash('Logged in','success')
                    return redirect(url_for('userdash'))
                else:
                    
                    flash("please register first and login","danger")
                    return redirect(url_for('login'))
            except:
                flash("please register first and login","danger")
                return redirect(url_for('login'))

    return render_template("login_page.html",form=form)

@app.route('/otpv',methods=['POST','GET'])
def otpv():  
    form=myform(request.form)
    email=form.email.data
    otpc=str(generateOTP())
    message = "Your OTP is "+ otpc
    session['otpc']=otpc     
    mail(email,message)
    print(otpc)
    data="otpdata"
    return render_template('reg.html',form=form,data=data)
    

#::::::::::::::::::::::::::::::::::::::::::::::::::::register page
@app.route('/register',methods=['POST','GET'])
def reg():
    form=myform(request.form)
    
    if request.method=='POST' and form.validate():
        fname=form.firstname.data
        lname=form.lastname.data
        phone=form.phone.data
        password=form.password.data
        email=form.email.data     
        otp=form.otp.data

        if(str(otp)==session.get('otpc')):
            with sqlite3.connect('r.db') as con:
                try:
                    cur=con.cursor()
                    cur.execute("INSERT INTO users (email,password,firstname,lastname,phone) VALUES (?,?,?,?,?)",(email,hashlib.md5(password.encode()).hexdigest(),fname,lname,phone))
                    con.commit()
                    flash("Registered Successfully",'success')
                except:
                    con.rollback()
                    flash("error occur")
            con.close()
            session.pop('otpc',None)
            return redirect(url_for('login'))
        else:
            flash("Invalid OTP",'danger')
            data="otpdata"
            return render_template('reg.html',form=form,data=data)
    else:
        data="nodata"
        return render_template('reg.html',form=form,data=data)
#::::::::::::::::::::::::::::::::::::::::::::profile edit
@app.route('/profileedit',methods=['POST','GET'])
def profileedit():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        phone=request.form['phone']
        email=session.get('email')
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            try:
                cur.execute("UPDATE users SET firstname=?,lastname=?,phone=? WHERE email=?",(fname,lname,phone,email))
                con.commit()
                flash("updated successfully","success")
                return redirect(url_for('userdash'))
            except:
                flash("error in updating","warning")
                return redirect(url_for('userdash'))
    email=session.get('email')
    with sqlite3.connect('r.db') as con:
        cur=con.cursor()
        data=0
        try:
            cur.execute("SELECT * FROM users WHERE email=?",(email,))
            data=cur.fetchone()
        except:
            flash("error","danger")
    return render_template("profileedit.html",data=data)

#::::::::::::::::::::::::::::::::::::::::::::password change
@app.route('/password',methods=['POST','GET'])
def password():
    form=passwordform(request.form)
    if request.method=='POST' and form.validate():
        email=session.get('email')
        old=form.old.data
        new=form.password.data
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            try:
                cur.execute("SELECT password FROM users WHERE email=?",(email,))
                data=cur.fetchone()
                if hashlib.md5(old.encode()).hexdigest() == data[0]:
                    cur.execute("UPDATE users SET password=? WHERE email=?",(hashlib.md5(new.encode()).hexdigest(),email))
                    con.commit()
                    flash("password changed successfully","success")
                    return redirect(url_for('userdash'))
                else:
                    flash("your old password is wrong","warning")
                    return redirect(url_for('userdash'))
            except:
                flash("no user","danger")
                return redirect(url_for('userdash'))
    return render_template("passwordchange.html",form=form)


                
#::::::::::::::::::::::::::::::::::::::::::::USERDASHBOARD
@app.route('/userdashboard')
def userdash():
    return render_template("userdashboard.html")


#::::::::::::::::::::::::::::::::::::::::::::::::::;LLR_DOWNLOADING
@app.route('/llrdownload',methods=['POST','GET'])
def llrdownload():
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
    
#:::::::::::::::::::::::::::::::::::::::::::::::::::::toshow pdff files
@app.route('/showpdf',methods=['GET','POST'])
def showpdf():
    if request.method=='POST':
        username=request.form['username']
        user=mongo.db.users.find_one({'username':username})
        filename=user['filename']
        return mongo.send_file(filename)
    return render_template("showpdf.html")

     
   
    
#:::::::::::::::::::::::::::::::::::::::::::::::::::llr   

@app.route("/llr",methods=["GET","POST"])
def llrapply():
    form=llr_user(request.form)
    if(request.method =='POST' and form.validate()):
        age=int(request.form['age'])
        if age>=18:
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
            dob=request.form['dob']
            age=request.form['age']
            gender=form.gender.data
            phone=form.phone.data
            bloodgroup=form.blood_group.data
            currentdate= date.today()
            expirydate = date.today()+timedelta(30)
            typee=request.form['typee']
            rtooffice=form.rtooffice.data
            with sqlite3.connect('r.db') as con:
                try:
                    cur=con.cursor()
                    cur.execute("SELECT code FROM rtocodes WHERE rto=?",(rtooffice,))
                    t=cur.fetchone()
                except:
                    print("error in selecting codes from database")
            con.close()
            now=datetime.now()
            number=random.randint(10000,80000)
            llrno=t[0]+ str(now.year) + str(number)


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
                    cur.execute("INSERT INTO llr (firstname,lastname,fathername,email,address,pincode,city,district,state,country,dob,age,gender,phone,bloodgroup,currentdate,expirydate,status,type,rto,llrno) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(firstname,lastname,fathersname,email,address,pincode,city,district,state,country,dob,age,gender,phone,bloodgroup,currentdate,expirydate,status,typee,rtooffice,llrno))
                    con.commit()
                
                    try:
                        mongo.save_file(aadharpdf.filename,aadharpdf)
                        mongo.save_file(sslcpdf.filename,sslcpdf)
                        mongo.save_file(voteridpdf.filename,voteridpdf)
                        mongo.save_file(signature.filename,signature)
                        mongo.save_file(photo.filename,photo)
                        mongo.db.users.insert({'email':email,'aadharpdf':aadharpdf.filename,'sslcpdf':sslcpdf.filename,'voterid':voteridpdf.filename,'signature':signature.filename,'photo':photo.filename})
                        flash("reg successfully")
                    except:
                        flash("mongo error")
                except:
                    con.rollback()
                    flash("error occur")
            con.close()
                
            return redirect(url_for('userdash'))
        else:
            flash("your age must be greater than 18 to apply LLR")
            return render_template("appllr.html",form=form)

        
    else:
        
        with sqlite3.connect('r.db') as con:
                try:
                    cur=con.cursor()
                    if(cur.execute("SELECT type FROM llr WHERE email=?",(session.get('email'),))):
                        t=cur.fetchone()
                        if t:
                            if(t[0]=="lmv:mcwg:tractor"):
                                flash("you already registered for all type of licences")
                                return redirect(url_for('userdash'))
                            else:
                                return redirect(url_for('oldllrupdate'))
                        else:
                            
                            return render_template("appllr.html",form=form)
                except:
                    flash("please retry ")
                    return redirect(url_for('userdash'))

#::::::::::::::::::::::::::::::::::::::::::OLD LLR update:::::::::::::::::;
@app.route('/oldllrupdate',methods=['GET','POST'])
def oldllrupdate():
    if request.method == 'POST':
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            typee=request.form.get('typee')
            email=session.get('email')
            cur.execute("UPDATE llr SET type=? WHERE email=?",(typee,email))
            con.commit()
                    
            flash("update successfully")
        return redirect(url_for('userdash'))
    with sqlite3.connect('r.db') as con:
        try:
            cur=con.cursor()
            cur.execute("SELECT type FROM llr WHERE email=?",(session.get('email'),))
            t=cur.fetchone()
            if t:
                if(t[0]=="lmv:mcwg:tractor"):
                    flash("you already registered for all type of licences")
                    return redirect(url_for('userdash'))
                else:
                    return render_template("oldllrupdate.html",t=t)
            else:
                flash("please retry ")
                return redirect(url_for('userdash'))
        except:
            flash("please retry ")
            return redirect(url_for('userdash'))
                
    return redirect(url_for('userdash'))

#::::::::::::::::::::::::::::::::::::::::::::::register vehicles

@app.route('/regv', methods=['GET','POST'])
def regv():
    form=regvehi(request.form)
    if request.method == 'POST' and form.validate():
            firstname=form.firstname.data
            lastname=form.lastname.data
            fathersname=form.fathersname.data
            email=form.email.data
            address=form.address.data
            enginenumber=form.enginenumber.data
            ownership=form.ownership.data
            vetype = form.vetype.data
            vclass = form.vclass.data
            purchasedate = form.purchasedate.data
            manufacture = form.manufacture.data
            modelname = form.modelname.data
            manufacturedate = form.manufacturedate.data
            fuel = form.fuel.data
            color = form.color.data
            insurencecompany = form.insurencecompany.data
            datefrom = form.datefrom.data
            dateto = form.dateto.data
            insurancenumber = form.insurancenumber.data
            pending = "pending"
            #PHOTOS 
            sideview = request.files["sideview"]
            frontview = request.files["frontview"]
            backview = request.files["backview"]
            mongo.save_file(sideview.filename,sideview)
            mongo.save_file(frontview.filename,frontview)              
            mongo.save_file(backview.filename,backview)
            mongo.db.vehicles.insert({'email':email,'enginenumber':enginenumber,'sideview':sideview.filename,'frontview':frontview.filename,'backview':backview.filename})
                    
                    

            with sqlite3.connect('r.db') as con:
                try:
                    cur=con.cursor()
                    cur.execute("INSERT INTO vehicle(firstname,lastname,fathersname,email,address,enginenumber,ownership,vetype,vclass,purchasedate,manufacture,modelname,manufacturedate,fuel,color,insurencecompany,datefrom,dateto,insurancenumber,status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(firstname,lastname,fathersname,email,address,enginenumber,ownership,vetype,vclass,purchasedate,manufacture,modelname,manufacturedate,fuel,color,insurencecompany,datefrom,dateto,insurancenumber,pending))
                    cur.commit()
                   
                except:
                    flash("Successfull Registered","success")
                
            return redirect(url_for('userdash'))
            flash("Registerd Successfully")
    else:
        
        return render_template("regv.html",form=form)

#:::::::::::::::::::::::::::::::::::::::::::::::::::status
@app.route('/status')
def status():
    try:
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
    except:
        flash("Please Apply For LLR First!","warning")
        return redirect(url_for('userdash'))
        
@app.route('/llrstatus')
def llrstatus():
    try:
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT status FROM llr WHERE email = ?",(session.get('email'),))
            st=cur.fetchone()
            if st[0] == "pending":
                return render_template("statuspending.html") 
            elif st[0] == "rejected":
                return render_template("statusdeclined.html")
            else:
                return render_template("statusaccepted.html")
            con.close()
    except:
        flash("Please Apply For LLR First!","warning")
        return redirect(url_for('userdash'))
        
@app.route('/dlrstatus')
def dlrstatus():
    try:
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT status FROM dlr WHERE email = ?",(session.get('email'),))
            st=cur.fetchone()
            if st[0] == "pending":
                return render_template("statuspending.html") 
            elif st[0] == "rejected":
                return render_template("statusdeclined.html")
            else:
                return render_template("statusaccepted.html")
            con.close()
    except:
        flash("Please Apply For DLR First!","warning")
        return redirect(url_for('userdash'))
@app.route('/vrstatus')
def vrstatus():
    try:
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT status FROM vehicle WHERE email = ?",(session.get('email'),))
            st=cur.fetchone()
            if st[0] == "pending":
                return render_template("statuspending.html") 
            elif st[0] == "rejected":
                return render_template("statusdeclined.html")
            else:
                return render_template("statusaccepted.html")
            con.close()
    except:
        flash("Please Apply For VR First!","warning")
        return redirect(url_for('userdash'))
   
    

#::::::::::::::::::::::::::::::DLR:::::::::::::::::::::::::::::::::::::::::::::::
@app.route('/dlr',methods=["GET","POST"])
def dlr():
    currentdate = date.today()
    expirydate = date.today()+timedelta(3650)
    if request.method=='POST':
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("INSERT INTO dlr(email,currentdate,expirydate,status,dlnumber) VALUES(?,?,?,?,?)",(session.get('email'),currentdate,expirydate,"pending","000000000"))
            con.commit()
        flash("Regestered Successfully","success")
        return render_template('userdashboard.html')


    with sqlite3.connect('r.db') as con:
        try:
            cur=con.cursor()
            cur.execute("SELECT status FROM llr WHERE email = ?",(session.get('email'),))
            st=cur.fetchone()
            if st[0] == "accepted":
                
                return render_template("appdlr.html")
            else:
               
                flash("Please Apply For LLR First","warning")
                return render_template('userdashboard.html')
        except:
            flash("Please Apply For LLR First","warning")
            return render_template('userdashboard.html')

#:::::::::::::::::::::::::::::::::::::::::::::::;llr download
@app.route('/dlllr')
def dlllr():
    acc = "accepted"
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            email=session.get('email')
            cur.execute("SELECT * FROM llr WHERE email=? AND status=?",(email,acc))
            data=cur.fetchone()
            if data:       
                rendered=render_template("llrform.html",data=data)
                pdf=pdfkit.from_string(rendered,False)
                response=make_response(pdf)
                response.headers['Content-Type']='application/pdf'
                response.headers['Content-Disposition']='attachment; filename=llr.pdf' #downloadable file 
                return response 
            else:
                flash("No LLR Found","danger")

    return render_template("userdashboard.html")
#::::::::::::::::::::::::::::::::::::::::::::::::::::::dlr download
@app.route('/dldlr')
def dldlr():
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            email=session.get('email')
            cur.execute("SELECT * FROM llr WHERE email=?",(email,))
            data=cur.fetchone() 
            cur.execute("SELECT * FROM dlr WHERE email=?",(email,))
            data1=cur.fetchone()
            try:
                if data1[3] == "accepted":     
                    rendered=render_template("dlrform.html",data=data)
                    pdf=pdfkit.from_string(rendered,False)
                    response=make_response(pdf)
                    response.headers['Content-Type']='application/pdf'
                    response.headers['Content-Disposition']='attachment; filename=dlr.pdf' #downloadable file 
                    return response
                else:
                    flash("No Drivers Licence Found","danger")
            except:
                flash("No Drivers Licence Found","danger")


    return render_template("userdashboard.html")

#::::::::::::::::::::::::::::::::::::::::::::vehicle register download:::::::
@app.route('/dlvr',methods = ["POST","GET"])
def dlvr():
    form=vrdl(request.form)
    
    if request.method=='POST' and form.validate():
        email = session.get('email')
        acc = "accepted"
        enginenumber=form.enginenumber.data
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM vehicle WHERE enginenumber=? AND email =? AND status=?",(enginenumber,email,acc)) 
            data=cur.fetchone()
            if data:
                rendered=render_template("vrdform.html",data=data)
                pdf=pdfkit.from_string(rendered,False)
                response=make_response(pdf)
                response.headers['Content-Type']='application/pdf'
                response.headers['Content-Disposition']='attachment; filename=vr.pdf' #downloadable file 
                return response                 
            else:
                flash("ERROR : Check Whether You Have Entered Valid ENGINE NUMBER and You have Registered Your vehicle","warning")
                
    return render_template("vdocdl.html")
    
                   

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::employee:::::::::::::::::::::::::::::::::::::::::
@app.route('/empdashboard')
def empdash():

    return render_template("empdashboard.html")

@app.route('/emplogin',methods=['POST','GET'])
def emplogin():
    form=emplogform(request.form)
    if request.method=='POST' and form.validate():
        empemail=form.email.data
        emppassword=form.password.data
        secretkey=form.secretkey.data
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            try:
                cur.execute("SELECT * FROM admin WHERE email=? and password=? and secretkey=?",(empemail,emppassword,secretkey))
                data=cur.fetchone()
                if data:
                    flash('Logged in','success')
                    session['email']=data[0]
                    session['logname']=data[3]
                    session['key']="admin"
                    return redirect(url_for('empdash'))
                else:
                    flash("please contact admin for registration","danger")
                    return redirect(url_for('home'))
            except:
                flash("please contact admin for registration","danger")
                return redirect(url_for('home'))

            
                

    return render_template("emplogin.html",form=form)



#######################################EMP LLR##############################################33333
@app.route('/adminllr',methods=['GET','POST'])
def adminllr():
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            try:
                if(cur.execute("SELECT firstname,email,age,city,gender,currentdate,type,applno FROM llr WHERE status=?",("pending",))):
                    data=cur.fetchall()
                    return render_template('adminllr.html',data=data)
                
            
                else:
                    flash("no user requests","warning")
                    return render_template('empdashboard.html')
            except:
                flash("no user requests","warning")
                return render_template('empdashboard.html')


   




@app.route('/aadhar/<email>',methods=['GET','POST'])
def getaadhar(email):
    user=mongo.db.users.find_one({'email':email})
    filename=user['aadharpdf']
    return mongo.send_file(filename)


@app.route('/voterid/<email>',methods=['GET','POST'])
def getvoterid(email):
    user=mongo.db.users.find_one({'email':email})
    filename=user['voterid']
    return mongo.send_file(filename)


@app.route('/sslc/<email>',methods=['GET','POST'])
def getsslc(email):
    user=mongo.db.users.find_one({'email':email})
    filename=user['sslcpdf']
    return mongo.send_file(filename)

@app.route('/details/<email>',methods=['GET','POST'])
def getdetails(email):
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM llr WHERE email=?",(email,))
            data=cur.fetchone()       
    rendered=render_template("adminllrform.html",data=data)
    pdf=pdfkit.from_string(rendered,False)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='attachment; filename=llr.pdf' #downloadable file 
    return response

@app.route('/edit/<email>',methods=['GET','POST'])
def updatellrdatabase(email):
     curdate = date.today()
     feedback=str(request.form.get('feedback'))
     accepted = "Your LLR Has Been Accepted"
     rejected = "Your LLR Has Been Rejected because "+feedback
     
     with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            
            if request.form['action'] == "accept":
                cur.execute("UPDATE llr SET status=?,admindate=?,feedback=? WHERE email=?",("accepted",curdate,feedback,email))
                mail(email,accepted)
                con.commit()
                return redirect(url_for('adminllr'))
            else:
                cur.execute("UPDATE llr SET status=?,admindate=?,feedback=? WHERE email=?",("rejected",curdate,feedback,email))
                mail(email,rejected)
                con.commit()
                return redirect(url_for('adminllr'))


########################################## EMP DLR ############################################
@app.route('/admindlr',methods=['GET','POST'])
def admindlr():
     with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            try:
                if(cur.execute("select firstname,email,age,city,gender,currentdate,type from llr where email in(select email from dlr where status = ?)",("pending",))):
                    data=cur.fetchall()
                    return render_template('admindlr.html',data=data)
                else:
                    flash("no user requests","warning")
                    return render_template('empdashboard.html')
            except:
                flash("no user requests","warning")
                return render_template('empdashboard.html')

     return render_template('admindlr.html')
@app.route('/dlredit/<email>',methods=['GET','POST'])
def updatedatabase(email):
     feedback=request.form.get('feedback')
     curdate = date.today()
     accepted = "Your DLR Has Been Accepted"
     rejected = "Your DLR Has Been Rejected:"+feedback
     with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            
            if request.form['action'] == "accept":
                cur.execute("UPDATE dlr SET status=?,admindate=?,feedback=? WHERE email=?",("accepted",curdate,feedback,email))
                
                con.commit()
                mail(email,accepted)
                return redirect(url_for('admindlr'))
            else:
                cur.execute("UPDATE dlr SET status=?,admindate=?,feedback=? WHERE email=?",("rejected",curdate,feedback,email))
                con.commit()
                mail(email,rejected)
                return redirect(url_for('admindlr'))

########################################EMP REGV####################################################


@app.route('/adminregv',methods=['GET','POST'])
def adminregv():
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            if(cur.execute("SELECT * FROM vehicle WHERE status=?",("pending",))):
                data=cur.fetchall()
                return render_template('adminregv.html',data=data)
            else:
                flash("error")
                return render_template('empdashboard.html')

    return render_template('adminregv.html')


@app.route('/frontview/<enginenumber>',methods=['GET','POST'])
def getfront(enginenumber):
    user=mongo.db.vehicles.find_one({'enginenumber':enginenumber})
    filename=user['frontview']
    return mongo.send_file(filename)
@app.route('/sideview/<enginenumber>',methods=['GET','POST'])
def getside(enginenumber):
    user=mongo.db.vehicles.find_one({'enginenumber':enginenumber})
    filename=user['sideview']
    return mongo.send_file(filename)
@app.route('/backview/<enginenumber>',methods=['GET','POST'])
def getback(enginenumber):
    user=mongo.db.vehicles.find_one({'enginenumber':enginenumber})
    filename=user['backview']
    return mongo.send_file(filename)

@app.route('/vehicledetails/<enginenumber>',methods=['GET','POST'])
def getvdetails(enginenumber):
    with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM vehicle WHERE enginenumber=?",(enginenumber,))
            data=cur.fetchone()       
    rendered=render_template("adminvrform.html",data=data)
    pdf=pdfkit.from_string(rendered,False)
    response=make_response(pdf)
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition']='attachment; filename=vr.pdf' #downloadable file 
    return response

@app.route('/vredit/<enginenumber>',methods=['GET','POST'])
def updatevdatabase(enginenumber):
     zero = "0000"
     curdate = date.today()
     vno = "KA"+str(random.randint(1000,9999))
     
     email = session.get('email')
     accepted = "Your vehicle registration request Has Been Accepted,your enginenumber is:"+str(enginenumber)
     rejected = "Your vehicle registration request Has Been Rejected:your enginenumber is:"+str(enginenumber)
     with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            
            if request.form['action'] == "accept":
                cur.execute("UPDATE vehicle SET status=?,admindate=?,vehiclenumber=? WHERE enginenumber=?",("accepted",curdate,vno,enginenumber))
                con.commit()
                mail(email,accepted)
                return redirect(url_for('adminregv'))
            else:
                cur.execute("UPDATE vehicle SET status=?,admindate=?,vehiclenumber=? WHERE enginenumber=?",("rejected",curdate,zero,enginenumber))
                con.commit()
                mail(email,rejected)
                return redirect(url_for('adminregv'))
#################################################EMP STATUS##############################################

@app.route('/adstatus',methods=['GET','POST'])
def adstatus():
    if request.method=='POST':
        date = request.form['date']
        typee=request.form['typee']
        with sqlite3.connect('r.db') as con:
            cur=con.cursor()
            if typee=="llr":
                cur.execute("SELECT applno,status FROM llr WHERE admindate=?",(date,))
            elif typee=="dlr":
                cur.execute("SELECT applno,status FROM dlr WHERE admindate=?",(date,))
            elif typee=="vehicle":
                 cur.execute("SELECT applno,status FROM vehicle WHERE admindate=?",(date,))
            data=cur.fetchall()
        return render_template("adstatus.html",data=data)
        
             
    data="none"
    return render_template("adstatus.html",data=data)

    


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#class uploadSSLC(Form):
 #   file = FileField()
 #   submit = SubmitField("Submit")
#class uploadADHAR(Form):
  ##  file = FileField()
    #submit = SubmitField("Submit")
"""class uploadllr(Form):
    file1 = FileField(validators=[FileRequired()])
    submit = SubmitField("Submit")
    file2 = FileField(validators=[FileRequired()])
    submit2 = SubmitField("Submit")
    file3 = FileField(validators=[FileRequired()])
    submit3 = SubmitField("Submit")
    check = BooleanField("Consent")


def llrdb(name,file1,file2,file3):
        with sqlite3.connect('r.db') as con:
        cursor=con.cursor()
        #cursor.execute("" CREATE table llr(uname TEXT,file1 BLOB,file2 BLOB,file3 BLOB)"")
        try:
            cursor.execute(" INSERT INTO llr(uname,file1,file2,file3) VALUES(?,?,?,?)",(name,file1,file2,file3))
        except:
            print("ERROR")
        con.commit()
        cursor.close()

        


def llrdb(file):
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
        cursor.close()


def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData



    

    
form=uploadllr(request.form)
        print("booo")
        if request.method=='POST' and form.validate(): #NOT GOING....
        print("YOO")  #FIX THIS
        llrdb(name="n",file1=form.file1.data.read(),file2=form.file2.data.read(),file3=form.file3.data.read())
        print("ERROR !")
        return "Request Submitted
    return render_template("applyllr.html")"""

   
if(__name__=="__main__"):
    app.run(debug=True)
