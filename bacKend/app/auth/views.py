from flask import request
from . import auth
from app import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

@auth.route('/token', methods=["POST"])
def create_token():

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
    
        role = '15'
        
        try:

            conn = mysql.connect.cursor()
            conn.execute('''INSERT INTO usersinformation(type_document,document,first_name,middle_name,first_last_name,second_last_name,address,cellphone,email,company_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (type_document,document,first_name,middle_name,first_last_name,second_last_name,address,cellphone,email,company_id))
            conn.connection.commit()
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


@auth.route('/login', methods=['GET','POST'])
def login():

    username = request.json['username']
    password = request.json['password']

    

    try:
        conn = mysql.connect.cursor()

        if("@" in username):
            
            # print(response)
            email = username
            conn.execute("SELECT * FROM user_login WHERE email = %s", (email,))
        
        else:

            conn.execute("SELECT * FROM user_login WHERE username = %s", (username,))
        
        value = [{"idul": a[0],"username":a[1],"email":a[2],"password":a[3],"role":a[4],"document":a[5]} for a in conn]

        conn.close()


        if len(value) > 0 and check_password_hash(value[0]["password"],password):
            access_token = create_access_token(identity=value[0]["idul"])
            print(access_token)
            # response = {"access_token":access_token}
            return 'True'
        else:
            return 'Password or username is incorrect'
        
    except Exception as e:

        print(e)
        return "Something wrong with the login"

@auth.route('/logout')
def logout():
    return 'User Logout'

