from flask import session, redirect, url_for, render_template, request, flash
from . import main
from .forms import LoginForm
import mysql.connector as sql
import cloudinary as cloud
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import time
global name
cn=sql.connect(user="root", password="admin", host="localhost", database="dating")
cr=cn.cursor(buffered=True)
cr.execute("Select name from users;")
name=cr.fetchall()
cr.execute("Select name, password from users;")
result=cr.fetchall()
print(result)
idpass={}
cloud.config( 
    cloud_name = "dlgyaawlm", 
    api_key = "233346284894765", 
    api_secret = "Dxb-iQJslyUwGFdwCJ5Ci0JDDLU", # Click 'View API Keys' above to copy your API secret
    secure=True
)

for i in result:
    idpass[i[0]]=i[1]
print(idpass)
@main.route('/')
def index():

    cr.execute("Select name, password from users;")
    result=cr.fetchall()
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html',tried=False)
    """Login form to enter a room."""
    '''form = LoginForm()'''
    '''if form.validate_on_submit():'''
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html',tried=False)
@main.post('/submitl')
def submitl():
    session['name'] = request.form["username"]
    session['password'] = request.form["password"]
    name = request.form["username"]
    password= request.form["password"]
    if idpass[name]==(password): 
        print("LOGIN BEHENCHOD")
        return redirect(url_for('.home'))
    else:
        return render_template('login.html', tried=True)
@main.post('/submitr')
def submitr():
    name = request.form["username"]
    password= request.form["password"]
    gender = request.form["gender"]
    age=request.form["age"]
    preferences=request.form["preferences"]
    state=request.form["state"]
    number=request.form["number"]
    photo=request.files["photo"]
    if name in idpass.keys():
        flash('username already exists!')
    upload_result = cloudinary.uploader.upload(photo, cloud_name="dlgyaawlm")
    url=upload_result["secure_url"]
    query="Insert into users values(%s, %s, %s, %s, %s, %s, %s, %s);"
    a=(name, number, gender, age, state, password, preferences,url)
    cr.execute(query,a)
    cn.commit()
    cr.execute("Select name, password from users;")
    result=cr.fetchall()
    for i in result:
        idpass[result[0][0]]=result[0][1]
    return redirect('/')


@main.route('/home')
def home():
    
    return render_template('home.html',name1=name[0])

@main.route(f'/meet/<name>')
def meet(name):
    query=("select photourl from users where name=%s")
    cr.execute(query,(name,))
    url=cr.fetchall()
    return render_template('swipe.html',urlreal=url)

@main.route('/chat', methods=['GET', 'POST'])
def chat():
    """Chat room. The users's name and room must be stored in
    the session."""
    return render_template('chat.html', name=name)
