from itsdangerous.url_safe import URLSafeTimedSerializer as TimedSerializer 
from itsdangerous import URLSafeTimedSerializer as Serializer
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from flask import current_app


class People(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64),unique=False)
    cellphone = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True, index=True)
    adress = db.Column(db.String(64))
    age = db.Column(db.String(64))
    status = db.Column(db.Boolean(db.Boolean()))
    profile_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self,fullname='',cellphone=' ',email=' ',adress=' ',age=' ', status=True, profile_id=' '):
        self.fullname = fullname
        self.cellphone = cellphone
        self.email = email
        self.adress = adress
        self.age = age
        self.status = status
        self.profile_id = profile_id
    
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

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    profile_id = db.relationship('People', backref='user_id', lazy='dynamic')
    confirmed = db.Column(db.Boolean, default=False)
    # role_id = db.Column(db.Integer)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:

            print(current_app.config['FLASKY_ADMIN'])
            print(self.email)
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if  self.role is None:
                self.role = Role.query.filter_by(default=True).first()

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
        # print(s)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    # def generate_confirmation_token(self):
    #     s = TimedSerializer(current_app.secret_key, 'confirmation')
    #     return s.dumps(self.id)
    
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

class Role(db.Model):
    __tablename__ = 'roles'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

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
            'Administrator':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
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

