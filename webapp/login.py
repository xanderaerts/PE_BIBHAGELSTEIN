from . import db
from flask import Blueprint, render_template,url_for,redirect,request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from .dbmodels import Users

login = Blueprint('login',__name__)


@login.route('/', methods = ["POST","GET"])
@login.route('/login', methods = ["POST","GET"])
def load_user():
    error = ""
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True) #remember,zorgt er voor dat we gaan opslagen in de sessie dat we zijn ingelogt
                return redirect(url_for('main.index'))
            else:
                error = 'Wrong password'
        else:
            error = 'User does not exist'
    return render_template("login.html",error=error)


@login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.load_user'))




@login.route('/adduser', methods = ["POST","GET"])
@login_required
def adduser():
    username = "Hooms"
    password = "Hooms"
    naam = "Ooms"
    voornaam = "Hannelore"
    from .dbmodels import Users
    new_user = Users(username=username,password=generate_password_hash(password),naam=naam,voornaam=voornaam)
    db.session.add(new_user)
    db.session.commit()
    print('user added')
    return render_template(url_for('/index'))
