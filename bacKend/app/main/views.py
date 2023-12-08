#-----Flask Packages-----
from flask import Flask,render_template,redirect,request, url_for
from flask_login import login_required, current_user

from ..models import User
#-----Main-----
from . import main
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission,User

#-----Database Models-----
from ..models import People,Balance,BalanceDate,Role

#-----Other packages-----
import locale

#-----Currency configuration-----
locale.setlocale(locale.LC_MONETARY, 'en_US.US-ASCII')

#-----Forms-----

#-----Routes-----



@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"

@main.route('/', methods=['Get','POST'])
@login_required
def index():
    return render_template('index.html')


@main.route('/home')
@login_required
def home():
    return render_template('home.html')

@main.route('/people', methods=['GET','POST'])
# @login_required
def viewpeople():
    # print('helo')
    if request.method == 'POST':

        fullname = request.form.get('fullname')
        cellphone = request.form.get('cellphone')
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        adress = request.form.get('adress')
        age = request.form.get('age')
        status = True
        idperson = 0 

        # user = People(fullname,cellphone,email,adress,age,status)
        userlogin = User(email=email,username=username,password=password)

        db.session.add(userlogin)
        db.session.commit()

        idperson = db.session.query(User.id).filter_by(email = email)
        for i in idperson:
            idperson = i[0]
        print(idperson)
        user = People(fullname,cellphone,email,adress,age,status,idperson)
        db.session.add(user)
        db.session.commit()

        # return redirect(url_for('main.viewpeople'))
        return 'True'

    if request.method == 'GET':

        som = db.session.query(People.id,People.fullname,People.cellphone,People.email,People.adress,People.age,People.status,People.profile_id)
        # resultPeople = [{"id":person[0],"fullname":person[1],"cellphone":person[2],"email":person[3],"adress":person[4],"age":person[5],"status":person[6],"profile_id":person[7]} for person in som if person[7] != current_user.id]
        resultPeople = [{"id":person[0],"fullname":person[1],"cellphone":person[2],"email":person[3],"adress":person[4],"age":person[5],"status":person[6],"profile_id":person[7]} for person in som];
        # print(resultPeople)
        
        peopleArgInformation = [
            (
                personInformation["id"],
                personInformation["fullname"],
                personInformation["cellphone"],
                personInformation["email"],
                personInformation["adress"],
                personInformation["age"],
                personInformation["status"]
            )
            for personInformation in resultPeople
        ]
        
        # return render_template('people.html',people=peopleArgInformation)
    
        return peopleArgInformation
    # return render_template('people.html')
    # return 'True'

@main.route('/delete/<string:id>')
def deletePeople(id):
    idpeople = db.session.query(People.profile_id).filter_by(id = id)
    idpeople2 = [{"id":people[0]} for people in idpeople]
    User.query.filter_by(id=idpeople2[0]["id"]).delete()
    People.query.filter_by(id = id).delete()
    # People.query.filter_by(id = id).update({"status":False})
    # User.query.filter_by(id=idpeople2[0]["idpeople"]).delete()
    db.session.commit()

    return redirect(url_for('main.viewpeople'))

@main.route('/update/<id>')
def peopleUpdate(id):

    som = db.session.query(People.id,People.fullname,People.cellphone,People.email,People.adress,People.age,People.status,People.profile_id).filter_by(id = id)
    resultPeople = [{"id":person[0],"fullname":person[1],"cellphone":person[2],"email":person[3],"adress":person[4],"age":person[5],"status":person[6],"profile_id":person[7]} for person in som]
    rolespeople = []
    for i in resultPeople:
        ro = i['profile_id']
        som2 = db.session.query(User.role_id).filter_by(id=ro)
        som3 = [{"role":som[0]} for som in som2]
        for i2 in som3:
            som4 = db.session.query(Role.name).filter_by(id=i2['role'])
            for some5 in som4:
                i['roleperson'] = some5[0]
        rolespeople.append(i)
    # print(rolespeople)
    peopleArgInformation = [
        (
            personInformation["id"],
            personInformation["fullname"],
            personInformation["cellphone"],
            personInformation["email"],
            personInformation["adress"],
            personInformation["age"],
            personInformation["status"],
            personInformation["profile_id"],
            personInformation["roleperson"]
        )
        for personInformation in rolespeople
    ]

    return render_template('updatepeople.html', person=peopleArgInformation)

@main.route('/updateperson/<id>', methods=['POST'])
def updatePersonInformation(id):

    if request.method == 'POST':
        
        fullname = request.form.get('fullname')
        cellphone = request.form.get('cellphone')
        email = request.form.get('email')
        adress = request.form.get('adress')
        age = request.form.get('age')
        status = request.form.get('statusperson')
        newstatus = True
        role_id = request.form.get('role')
        id_user = request.form.get('profile_id')
        print(role_id)
        if status == 'Desactivate':
            newstatus = False
        db.session.query(User).filter_by(id=id_user).update({"role_id":role_id})
        db.session.commit()
        db.session.query(People).filter_by(id=id).update({"fullname":fullname,"cellphone":cellphone,"email":email,"adress":adress,"age":age,"status":newstatus})
        db.session.commit()
        
        return redirect('/people')

@main.route('/adddetail', methods=['GET','POST'])
def seePeopleDetails():

    if request.method == 'GET':
        som = db.session.query(People.id,People.fullname,People.status)
        peopleInformationdetail = [{"id":person[0],"fullname":person[1]} for person in som if person[2] == True]
        
        peopleArgInformation = [
            (
                personInformation["id"],
                personInformation["fullname"],
            )
            for personInformation in peopleInformationdetail
        ]
        return render_template('adddetails.html',namespeople=peopleArgInformation)
    
    if request.method == 'POST':
        
        fullname  = "{}".format(request.form.get('fullname')).split(', ')
        print(fullname)
        name2 = []
        number = []
        monto = request.form.get("total")
        datedetail = request.form.get("dateregistered")
        detail = request.form.get("tipo")

        for name in request.form.get('fullname'):
            if name.isnumeric(): 
                number.append(name)
            else:
                name2.append(name)

        person_id = "".join(number)
        print(person_id)
        som = db.session.query(Balance.monto).filter_by(person_id=person_id)
        peopleInformationdetail = [{"monto":person[0]} for person in som]

        if detail != 'Gasto':
            if len(peopleInformationdetail) == 1:
                for i in peopleInformationdetail:
                    montofinal = int(i['monto']) + int(monto)
                db.session.query(Balance).filter_by(person_id=person_id).update({"monto":montofinal})
            else:
                user = Balance(person_id,monto)
                db.session.add(user)

        user = BalanceDate(person_id,detail,monto,datedetail)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/adddetail')

@main.route('/balance', methods=['POST','GET'])
def showBalanceTable():

    if request.method == 'GET':
        som = db.session.query(Balance.person_id,Balance.monto)
        peopleInformationdetail = [{"person_id":person[0],"monto":person[1]} for person in som]
        # print(peopleInformationdetail)
        person = []

        for i in peopleInformationdetail:
            person_id = i['person_id']
            # print(person_id)
            names = db.session.query(People.id, People.fullname).filter_by(id=person_id)
            peopleInformationdetailNames = [{"id":person[0],"fullname":person[1]} for person in names]
            print(peopleInformationdetailNames)
            fullname=''

            for a in peopleInformationdetailNames:
                fullname = a['fullname']

            monto = i["monto"]

            personinformation = {
                "person_id":person_id,
                "fullname":fullname,
                "monto":monto
            }
            
            person.append(personinformation)

        balancePeople = [
            (
                personBalance['person_id'],
                personBalance['fullname'],
                locale.currency(int(personBalance['monto'])),
            )
            for personBalance in person
        ]
        # print(balancePeople)

        return render_template('balance.html',balancePeople=balancePeople)

@main.route('/updatebalance/<id>', methods=['GET','POST'])
def updatebalance(id):

    names = db.session.query(Balance.person_id,Balance.monto).filter_by(person_id=id)
    peopleInformationdetailNames = [{"person_id":person[0],"monto":person[1]} for person in names]
    
    personInformationReady = [
        (
            personReady['person_id'],
            personReady['monto']
        )
        for personReady in peopleInformationdetailNames
    ]

    return render_template('updatebalance.html', personReady=personInformationReady)

@main.route('/updatebalanceinformation', methods=['GET','POST'])
def updatebalanceinfo():

    if request.method == 'POST':
        person_id = request.form.get('person_id') 
        reason = request.form.get('reason')
        savemonto = 0
        newmonto = int(request.form.get('newmonto'))
        monto2 = db.session.query(Balance.monto).filter_by(person_id=person_id)
        firstMonto = [{"monto":mon[0]} for mon in monto2]
        f1 = int(firstMonto[0]['monto'])

        if reason == 'Add':
            savemonto = f1 + newmonto
        elif reason == 'Subtract':
            savemonto = f1 - newmonto

        db.session.query(Balance).filter_by(person_id=person_id).update({"monto":savemonto})
        db.session.commit()

    return redirect('/balance')

@main.route('/churchbalanceperson', methods=['GET'])
def churchbalanceperson():
    som2 = db.session.query(User.email).filter_by(id=current_user.id)
    resul = [{"id":personid[0]} for personid in som2]
    som3 = db.session.query(People.id).filter_by(email=resul[0]['id'])
    resul3 = [{"id":personid[0]} for personid in som3]
    # print(current_user.id)
    # print(resul3)
    som = db.session.query(BalanceDate.id,BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto,BalanceDate.datedetail).filter_by(person_id=resul3[0]['id'])
    resultPeople = [{"id":person[0],"person_id":person[1],"detail":person[2],"monto":person[3],"datedetail":person[4]} for person in som]
    # print(resultPeople)
    ofrenda = 0
    diezmo = 0
    donation = 0
    gasto = 0
    for i in resultPeople:
        if i['detail'] == 'Ofrenda':
            ofrenda = ofrenda + int(i['monto'])
        if i['detail'] == 'Diezmo':
            diezmo = diezmo + int(i['monto'])
        if i['detail'] == 'Donation':
            donation = donation + int(i['monto'])
        if i['detail'] == 'Gasto':
            gasto = gasto + int(i['monto']) 

    total = (ofrenda + diezmo + donation) - gasto
    conta = [
        {
            "ofrenda":ofrenda,
            "diezmo":diezmo,
            "donation":donation,
            "gasto":gasto,
            "total":total
        }
    ]

    churchBalance = [
        (
            locale.currency(churchinformation['ofrenda']),
            locale.currency(churchinformation['diezmo']),
            locale.currency(churchinformation['donation']),
            locale.currency(churchinformation['gasto']),
            locale.currency(churchinformation['total'])
        )
        for churchinformation in conta
    ]
    
    return render_template('churchbalanceperson.html', churchbalance=churchBalance)
    
@main.route('/churchbalance',methods=['GET'])
def churchbalance():

    som = db.session.query(BalanceDate.id,BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto,BalanceDate.datedetail)
    resultPeople = [{"id":person[0],"person_id":person[1],"detail":person[2],"monto":person[3],"datedetail":person[4]} for person in som]
    ofrenda = 0
    diezmo = 0
    donation = 0
    gasto = 0

    for i in resultPeople:
        if i['detail'] == 'Ofrenda':
            ofrenda = ofrenda + int(i['monto'])
        if i['detail'] == 'Diezmo':
            diezmo = diezmo + int(i['monto'])
        if i['detail'] == 'Donation':
            donation = donation + int(i['monto'])
        if i['detail'] == 'Gasto':
            gasto = gasto + int(i['monto']) 

    total = (ofrenda + diezmo + donation) - gasto
    conta = [
        {
            "ofrenda":ofrenda,
            "diezmo":diezmo,
            "donation":donation,
            "gasto":gasto,
            "total":total
        }
    ]

    churchBalance = [
        (
            locale.currency(churchinformation['ofrenda']),
            locale.currency(churchinformation['diezmo']),
            locale.currency(churchinformation['donation']),
            locale.currency(churchinformation['gasto']),
            locale.currency(churchinformation['total'])
        )
        for churchinformation in conta
    ]
    
    return render_template('churchbalance.html', churchbalance=churchBalance)

@main.route('/historychurch', methods=["GET","POST"])
def historychurch():

    if request.method == 'POST':
        datedetailselect = request.form.get('datepeople')
        something = request.form.get('datepeopleyear')
        if len(datedetailselect) > 0 and len(something) > 0:
            something = ''
        if len(datedetailselect) == 0 and len(something) == 0:
            return redirect(url_for('main.historychurch'))
        elif len(datedetailselect) == 0:
            som = db.session.query(BalanceDate.id,BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto,BalanceDate.datedetail)
            resultPeople = [{"id":person[0],"person_id":person[1],"detail":person[2],"monto":person[3],"datedetail":person[4]} for person in som if something in person[4] and person[2] != 'Gasto']
        elif len(something) == 0:
            som = db.session.query(BalanceDate.id,BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto,BalanceDate.datedetail).filter_by(datedetail=datedetailselect)
            resultPeople = [{"id":person[0],"person_id":person[1],"detail":person[2],"monto":person[3],"datedetail":person[4]} for person in som if person[2] != 'Gasto']

        if len(resultPeople) == 0:
            return redirect(url_for('main.historychurch'))
        else:
            hystory = []
            people = []

            for history in resultPeople:
                id_principal = history["id"]
                id = history["person_id"]
                fullname = db.session.query(People.fullname).filter_by(id=id)
                lastnamef = [{"lastname":name[0]} for name in fullname]
                name = ''

                for i in lastnamef:
                    name = i['lastname']

                detail = history["detail"]
                monto = history["monto"]
                datedetail = history["datedetail"]
                hys =  {
                    "id_p":id_principal,
                    "person_id":id,
                    "fullname":name,
                    "detail":detail,
                    "monto":monto,
                    "datedetail":datedetail
                }
                hystory.append(hys)
                people.append(hys)

            person = {}

            for i in range(len(people)):
                if people[i]['fullname'] not in person:
                    person[people[i]['fullname']] = 0
            for i in range(len(people)):
                for a in person:
                    if people[i]['fullname'] == a:
                        person[people[i]['fullname']] =  person[a] + int(people[i]['monto'])
        
            people.clear()
    
            for i in person:
                name = {
                    'fullname':i,
                    'monto':person[i]
                }
                people.append(name)

            historychurch = [
                (
                    history["fullname"],
                    history["monto"]
                )
                
                for history in people
            ]

            return render_template('historychurch.html', historychurch2=historychurch)

    som = db.session.query(BalanceDate.id,BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto,BalanceDate.datedetail)
    resultPeople = [{"id":person[0],"person_id":person[1],"detail":person[2],"monto":person[3],"datedetail":person[4]} for person in som]
    hystory = []

    for history in resultPeople:
        id_principal = history["id"]
        id = history["person_id"]
        fullname = db.session.query(People.fullname).filter_by(id=id)
        lastnamef = [{"lastname":name[0]} for name in fullname]
        name = ''

        for i in lastnamef:
            name = i['lastname']

        detail = history["detail"]
        monto = history["monto"]
        datedetail = history["datedetail"]
        hys =  {
            "id_principal":id_principal,
            "id":id,
            "fullname":name,
            "detail":detail,
            "monto":monto,
            "datedetail":datedetail
        }
        hystory.append(hys)

    historychurch = [
        (
            history["id_principal"],
            history["id"],
            history["fullname"],
            history["detail"],
            history["monto"],
            history["datedetail"]
        )
        
        for history in hystory
    ]
    return render_template('historychurch.html',historychurch=historychurch)

# App.config['PDF_FOLDER'] = 'static/pdf'
# App.config['TEMPLATE_FOLDER'] = 'templates/'

@main.route('/historypersondelete/<string:id>')
def historypersondelete(id):

    som = db.session.query(BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto).filter_by(id=id)
    resultsom = [{"person_id":son[0],"monto":son[2]} for son in som if son[1] != "Gasto"]

    for i in resultsom:
        som2 = db.session.query(Balance.monto).filter_by(person_id=i['person_id'])
        resultsom2 = [{"monto":son[0]} for son in som2]
        for a in resultsom2:
            montofinal  = int(a['monto']) - int(i['monto'])
            db.session.query(Balance).filter_by(person_id=i['person_id']).update({"monto":montofinal})
            db.session.commit()
    db.session.query(BalanceDate).filter_by(id=id).delete()
    db.session.commit()

    return redirect('/historychurch')

@main.route('/historypersonupdate/<string:id>')
def historypersonupdate(id):
    som = db.session.query(BalanceDate.id,BalanceDate.person_id,BalanceDate.detail,BalanceDate.monto,BalanceDate.datedetail).filter_by(id=id)
    resultPeople = [{"id":person[0],"person_id":person[1],"detail":person[2],"monto":person[3],"datedetail":person[4]} for person in som]
    
    historychurch = [
        (
            history["id"],
            history["person_id"],
            history["detail"],
            history["monto"],
            history["datedetail"]
        )
        
        for history in resultPeople
    ]

    return render_template('/historypersonupdate.html',hystorypersonupdate=historychurch)

@main.route('/historypersonupdatenew/<string:id>', methods=['POST','GET'])
def historypersonupdatenew(id):
    
    if request.method == "POST":
        personid = request.form.get('personid')
        tipo = request.form.get('tipo')
        monto = request.form.get('monto')
        oldmonto = request.form.get('oldmonto')
        datedetail = request.form.get('datedetail')
        oldtipo = request.form.get('oldtipo')

        if tipo == 'Gasto':
            som = db.session.query(Balance.monto).filter_by(person_id=personid)
            dates = [{"monto":son[0]} for son in som]
            newmonto = 0
            for i in dates:
                newmonto  = int(i['monto']) - int(monto)
            db.session.query(Balance).filter_by(person_id=personid).update({"monto":newmonto})
            db.session.commit()
        else:
            som = db.session.query(Balance.monto).filter_by(person_id=personid)
            dates = [{"monto":son[0]} for son in som]
            newmonto2 = 0
            for i in dates:
                if oldtipo == 'Gasto':
                    newmonto2 = int(i['monto']) + int(monto)
                else:
                    montofinal = int(oldmonto) - int(monto)
                    if int(montofinal) < int(monto):
                        newmonto2 = int(i['monto']) - montofinal
                    else:
                        newmonto2 = int(i['monto']) - int(oldmonto)
                        newmonto2 = int(i['monto']) + int(monto)

            db.session.query(Balance).filter_by(person_id=personid).update({"monto":newmonto2})
            db.session.commit()

        db.session.query(BalanceDate).filter_by(id=id).update({"detail":tipo,"monto":monto,"datedetail":datedetail})
        db.session.commit()

        return redirect('/historychurch')
    
@main.route('/peopleinformaprofile', methods=['POST','GET'])
def peopleinformaprofile():
    # personinformation = db.session.commit(People.email).filter_by(profile_id=current_user.id)
    # if personinformation.length > 0:

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        cellphone = request.form.get('cellphone')
        email = request.form.get('email')
        adress = request.form.get('adress')
        age = request.form.get('age')
        status = True
        profile_id = request.form.get('idperson')

        user = People(fullname,cellphone,email,adress,age,status,profile_id)

        db.session.add(user)
        db.session.commit()

        redirect(url_for('main.home'))
    som = db.session.query(People.id,People.fullname,People.cellphone,People.email,People.adress,People.age,People.status,People.profile_id).filter_by(profile_id=current_user.id)
    resultPeople = [{"id":person[0],"fullname":person[1],"cellphone":person[2],"email":person[3],"adress":person[4],"age":person[5],"status":person[6],"profile_id":person[7]} for person in som]
    print(resultPeople)
    peopleArgInformation = [
        (
            personInformation["id"],
            personInformation["fullname"],
            personInformation["cellphone"],
            personInformation["email"],
            personInformation["adress"],
            personInformation["age"],
        )
        for personInformation in resultPeople
    ]
    print(peopleArgInformation)
    return render_template('/peopleinformaprofile.html', peopleArgInformation=peopleArgInformation)

@main.route('/peopleinformaprofile/<id>', methods=['GET','POST'])
def peopleinformaprofileupdate(id):
    id = id
    fullname = request.form.get('fullname')
    cellphone = request.form.get('cellphone')
    email = request.form.get('email')
    adress = request.form.get('adress')
    age = request.form.get('age')

    db.session.query(People).filter_by(id=id).update({"fullname":fullname,"cellphone":cellphone,"email":email,"adress":adress,"age":age})
    db.session.commit()
    
    return redirect(url_for('main.index'))
    
@main.route('/userslogin', methods=['GET','POST'])
def userslogininfo():
    userspeople = db.session.query(User.id, User.email, User.username, User.password_hash, User.confirmed)
    userpeopleinformation = [{"id":person[0],"email":person[1],"username":person[2],"password":person[3],"confirmed":person[4]} for person in userspeople]
    print(userpeopleinformation)
    userpeopleinformationfinal = [
        (
            people['id'],
            people['email'],
            people['username'],
            people['password'],
            people['confirmed']
        )
        for people in userpeopleinformation
    ]
    return render_template('/userlogin.html', userpeopleinformationfinal=userpeopleinformationfinal)

@main.route('/userlogin/<id>', methods=['GET','POST'])
def userloginupdate(id):
    userspeople = db.session.query(User.id, User.email, User.username, User.password_hash, User.confirmed).filter_by(id=id)
    userpeopleinformation = [{"id":person[0],"email":person[1],"username":person[2],"password":person[3],"confirmed":person[4]} for person in userspeople]
    userpeopleinformationfinal = [
        (
            people['id'],
            people['email'],
            people['username'],
            people['password'],
            people['confirmed']
        )
        for people in userpeopleinformation
    ]
    return render_template('/userloginupdate.html', userpeopleinformationfinal=userpeopleinformationfinal)

@main.route('/updateuser/<id>', methods=['GET','POST'])
def updateuser(id):
    user = User.query.get_or_404(id)
    email = request.form.get('email')
    password = request.form.get('password')
    user.email = email
    user.password = password
    # userpeople = User
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('main.index'))