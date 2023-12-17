from flask import redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User,db,People
from .forms import LoginForm



@auth.route('/login', methods=['GET','POST'])
def login():

    username = request.json['username']
    password = request.json['password']

    email = username
    password = password

    try:
            
        user = User.query.filter_by(email=email).first()
        active = False

        if user != None:
            active = True

        if user is not None and user.verify_password(password) and active is not False:
            return 'True';
        return 'False';
    except:
        print("Something wrong with the login")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    fullname = request.json['fullname']
    user = User(email=username,
                username=username,
                password=password)
    email= username
    db.session.add(user)

    userinformation = db.session.query(User.id).filter_by(email=email)
    idperson = [{"idperson":person[0]} for person in userinformation]
    profile_id = idperson[0]["idperson"]
    # print(profile_id)
    userpeople = People(fullname=fullname, email=email, profile_id=profile_id)
    db.session.add(userpeople)
    db.session.commit()

    return "Saved"
