from flask import Flask,render_template,request,flash,redirect,url_for
from wtforms import Form,StringField,PasswordField,validators,SubmitField
app=Flask(__name__)
#validating the register fields
class myform(Form):
    username=StringField('Username',[validators.Length(min=3,max=10)])
    email=StringField('Email',[validators.Length(min=3,max=10),validators.DataRequired()])
    password=PasswordField('NewPassword',[validators.DataRequired()])
    confirm=PasswordField('confirm')
    submit=SubmitField('send')
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
        flash('thaks for register')
        uname=form.username.data
        return render_template('test.html',uname=uname)
    else:
        flash('nnnnnnnn')
    return render_template('reg.html',form=form)
@app.route('/')
def test():
    data="nandish"
    return render_template('test.html',dataa=data)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        user=request.form['email']
        if (user=="nandish@gmail.com"):
            return redirect(url_for("test"))
    return render_template("login_page.html")

if(__name__=="__main__"):
    app.run(debug=True)
