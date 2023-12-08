from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User,db,People
from .forms import LoginForm, RegistrationForm



@auth.route('/login', methods=['GET','POST'])
def login():

    username = request.json['username']
    password = request.json['password']

    form = LoginForm()
    email = username
    password = password
    user = User.query.filter_by(email=email).first()
    active = True

    
    if user is not None and user.verify_password(password) and active is not False:
        # print('verified')
        login_user(user, form.remember_me.data)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.index')
        return 'True';
    return 'False';

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    # form = RegistrationForm()
    username = request.json['username']
    password = request.json['password']
    fullname = request.json['fullname']
    # print(username)
    # print(password)
    # if form.validate_on_submit():
    user = User(email=username,
                username=username,
                password=password)
    email= username
    # people = People(user)
    db.session.add(user)
    # db.session.add(people)
    # People.session.commit()
    # db.session.commit()

    userinformation = db.session.query(User.id).filter_by(email=email)
    idperson = [{"idperson":person[0]} for person in userinformation]
    profile_id = idperson[0]["idperson"]
    print(profile_id)
    userpeople = People(fullname=fullname, email=email, profile_id=profile_id)
    db.session.add(userpeople)
    db.session.commit()
    
    # flash('You can now login.')
    # flash('A comfirmation email has been sent to your by email')
    return "Saved"
    # return render_template('auth/register.html', form=form)
