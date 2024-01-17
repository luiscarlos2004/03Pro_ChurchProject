from itsdangerous.url_safe import URLSafeTimedSerializer as TimedSerializer 
from itsdangerous import URLSafeTimedSerializer as Serializer
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from .. import login_manager
from flask import current_app

class Company(UserMixin,db.Model):
    __tablename__ = 'company'
    idc = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.String(64))
    company_id = db.Column(db.Integer, unique=True)
    foundation_date = db.Column(db.String(64))
    owners = db.relationship('People', backref='company')
    
    def __init__(self,company_name,company_id,foundation_date):
        self.company_name = company_name
        self.company_id = company_id
        self.foundation_date = foundation_date

class People(db.Model):
    __tablename__ = 'people'
    ido = db.Column(db.Integer, autoincrement=True)
    type_document = db.Column(db.String(64))
    document = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    first_last_name = db.Column(db.String(64))
    second_last_name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    cellphone = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.Integer)
    profile_id = db.relationship('User', backref='people', lazy='dynamic')
    company_id = db.Column(db.Integer, db.ForeignKey('company.idc'), nullable=False)

    def __ini__(self,type_document,document,first_name,middle_name,first_last_name,second_last_name,address,cellphone,email):
        self.type_document = type_document
        self.document = document
        self.first_name = first_name
        self.middle_name = middle_name
        self.first_last_name = first_last_name
        self.second_last_name = second_last_name
        self.address = address
        self.cellphone = cellphone
        self.email = email


class Role(db.Model):
    __tablename__ = 'roles'
    idr =  db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='roles', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0
    
    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
            'Company':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }

        default_role = 'User'

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    idu = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.idr'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('people.document'), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_active(self):
       return True
    
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True



# class People(db.Model):
    
#     id = db.Column(db.Integer, primary_key=True)
#     fullname = db.Column(db.String(64),unique=False)
#     cellphone = db.Column(db.Integer)
#     email = db.Column(db.String(64), unique=True, index=True)
#     adress = db.Column(db.String(64))
#     age = db.Column(db.String(64))
#     status = db.Column(db.Boolean(db.Boolean()))
#     profile_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # def __init__(self,fullname='',cellphone=' ',email=' ',adress=' ',age=' ', status=True, profile_id=' '):
    #     self.fullname = fullname
    #     self.cellphone = cellphone
    #     self.email = email
    #     self.adress = adress
    #     self.age = age
    #     self.status = status
    #     self.profile_id = profile_id
    
class Balance(db.Model):

    person_id = db.Column(db.String(64), unique=True, primary_key=True)
    monto = db.Column(db.String(64))

    def __init__(self, person_id, monto):
        self.person_id = person_id
        self.monto = monto

class BalanceDate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.String(64))
    detail = db.Column(db.String(64))
    monto = db.Column(db.String(64))
    datedetail = db.Column(db.String(64))

    def __init__(self, person_id, detail, monto, datedetail):
        self.person_id = person_id
        self.detail = detail
        self.monto = monto
        self.datedetail = datedetail



class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False
    
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

