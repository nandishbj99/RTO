from flask import *
from wtforms import Form,StringField,PasswordField,validators,SubmitField,TextField,IntegerField
import sqlite3,hashlib,os
app=Flask(__name__)
#togetlogin details:
def getlogindetails():
    with sqlite3.connect('rto.db') as conn:
        cur=conn.cursor()
        if 'email' not in session:
            loggedIn=False
            loggeduname=""
        else:
            cur.execute("SELECT firstname,lastname FROM users WHERE email= ?",(session['email']))
            fname,lname=cur.fetchone()
            loggeduname=fname+""+lname
    conn.close()
    return (loggedIn,loggeduname)



#validating the register fields
class myform(Form):
    firstname=StringField('Firstname',[validators.Length(min=3,max=10)])
    email=TextField('Email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('NewPassword',[validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm=PasswordField('confirmPassword')
    lastname=StringField('Lastname',[validators.Length(min=1,max=10)])
    phone=IntegerField("Phone")



class mylogform(Form):
    email=TextField('email',[validators.Email(),validators.DataRequired()])
    password=PasswordField('password',[validators.DataRequired()])
app.secret_key='nandish'



@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register',methods=['POST','GET'])
def reg():
    form=myform(request.form)
    if request.method=='POST' and form.validate():
        fname=form.firstname.data
        lname=form.lastname.data
        phone=form.phone.data
        password=form.password.data
        email=form.email.data
        with sqlite3.connect('rto.db') as con:
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


@app.route('/')
def home():
    loggedIn, loggeduname=getlogindetails()

    
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    form=mylogform(request.form)
    if request.method=='POST' and form.validate():
        useremail=form.email.data
        upassword=form.password.data
        with sqlite3.connect('rto.db') as con:
            cur=con.cursor()
            cur.execute("SELECT email,password FROM users")
            data=cur.fetchall()
            for row in data:
                if row[0]==useremail and row[1] == hashlib.md5(upassword.encode()).hexdigest():
                    session['email']=useremail
                    return redirect(url_for('home'))
                else:
                    flash("please register first and login")
                    return redirect(url_for('home'))

    return render_template("login_page.html",form=formm)

if(__name__=="__main__"):
    app.run(debug=True)
