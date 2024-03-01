from flask import redirect, url_for, flash, request, jsonify
from flask_login import logout_user, login_required
from . import auth
from ..models import User,db,People
from app import mysql
from werkzeug.security import generate_password_hash, check_password_hash



# @auth.route('/testdatabaseadd', methods=['GET'])
# def testDatabase():
#     cursor = mysql.connect.cursor()
#     res = cursor.execute('''SELECT * FROM test''')
#     cursor.close()
#     return jsonify(res)

# @auth.route('/testdatabaseadd', methods=['POST'])
# def testdatabaseadd():
#     cursor = mysql.connect.cursor()
#     cursor.execute('''INSERT INTO test(name) VALUES(%s)''', ['carlos'])
#     cursor.connection.commit()
#     cursor.close()
#     return 'yea'

@auth.route('/registercompany', methods=['POST'])
def registercompany():

    try:

        company_name = request.json['company_name']
        company_id = request.json['company_id']
        foundation_date = request.json['foundation_date']
        owners = request.json['owners']

        try:

            conn = mysql.connect.cursor()
            conn.execute('''INSERT INTO companies(company_name,company_id,foundation_date,owners) VALUES(%s,%s,%s,%s)''', (company_name,company_id,foundation_date,owners))
            conn.connection.commit()
            conn.close()

        except:

            return 'Something went wrong with the database'
        
        else:

            return 'Information saved'
    except:
         
         return 'Something went wrong with the input values'

@auth.route('/registerperson', methods=['POST'])
def registerperson():

    try:

        type_document = request.json['type_document']
        document = request.json['document']
        first_name = request.json['first_name']
        middle_name = request.json['middle_name']
        first_last_name = request.json['first_last_name']
        second_last_name = request.json['second_last_name']
        address = request.json['address']
        cellphone = request.json['cellphone']
        email = request.json['email']
        company_id = request.json['company_id']

        username = request.json['username']
        password = generate_password_hash(request.json['password'])
        print(password)
        # @password.setter
        # def password(self, password):
        #     self.password_hash = generate_password_hash(password)

        # role = request.json['role']
        role = '15'
        
        try:

            conn = mysql.connect.cursor()
            conn.execute('''INSERT INTO usersinformation(type_document,document,first_name,middle_name,first_last_name,second_last_name,address,cellphone,email,company_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (type_document,document,first_name,middle_name,first_last_name,second_last_name,address,cellphone,email,company_id))
            # conn.execute('''INSERT INTO user_login(username,email,password,role,document) VALUES(%s,%s,%s,%s,%s)''',(username,email,password,role,document))
            # conn.connection.commit()
            conn.execute('''INSERT INTO user_login(username,email,password,role,document) VALUES(%s,%s,%s,%s,%s)''',(username,email,password,role,document))
            conn.connection.commit()
            conn.close()
            
        except Exception as error:
            print(error)
            return 'Something went wrong on the database'
        
        else:

            return 'Information saved'
        
    except:

        return 'Something went wrong with the input values'

@auth.route('/registeruser', methods=['GET','POST'])
def registeruser():
    pass

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
