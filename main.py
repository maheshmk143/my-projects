from flask import Flask,render_template, request,session
# from flask_mail import Mail 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# render_template is mainly used for add files with your code like html files

with open("config.json","r") as c:

    params=json.load(c)["params"]
local_server=True
app = Flask(__name__)
app.secret_key = 'super-secret-key'


#    direct send mail to your actual gmail account use below functios. 
# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=params['user_mail'],
#     MAIL_PASSWORD=params['password']
# )
# mail=Mail(app)

if local_server:

    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["proud_uri"]

# using flask sqlalchemy. go to quick start.
db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    sno,name,email,phone_num,mesg,date
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    phone_num = db.Column(db.String(120),  nullable=False)
    mesg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(120),  nullable=True)




class Posts(db.Model):
    '''sno,slug,title,content,date'''
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    tag_line = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=True)
    img_file=db.Column(db.String(12),nullable=True)



@app.route("/dashboard",methods=['GET','POST'])
def dashboard():

    if ('user' in session and session['user']==params['admin']):
        posts=Posts.query.all()
        return render_template('dashboard.html',params=params,posts=posts)

    if request.method=="POST":
        username=request.form.get('uname')
        userpass=request.form.get('pass')
        if (username==params['admin'] and userpass==params['admin_password']):
            # set the session variable
            session['user']=username
            posts=Posts.query.all()
            return render_template('dashboard.html',params=params,posts=posts)
    # redirect to admin panel
    return render_template("login.html",params=params)



@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:3]
    return render_template("index.html",params=params,posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

 # <string_slug> is used for slug.
@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()




    return render_template("post.html",params=params,post=post)


@app.route("/contact",methods=['GET', 'POST'])
def contact():
    '''Add Entry to the Data Base'''
    if (request.method=="POST"):
        name=request.form.get("name")
        email=request.form.get("email")
        phone=request.form.get("phone")
        msg=request.form.get("msg")
        
        entry=Contacts(name=name,email=email,phone_num=phone,date=datetime.now(),mesg=msg)
        db.session.add(entry)
        db.session.commit()
        # mail.send_message('New Message from '+name
        # ,sender=email,recipients=[params['user_mail']],
        # body=msg+ '\n'+ phone

        #      )

    return render_template("contact.html",params=params)

app.run(debug=True) # app.run is used for rune your code 
