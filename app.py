from flask        import Flask, request, render_template, redirect, url_for, session, flash
from datetime     import datetime
import pyrebase
import uuid

from protected import login_required
from firebase_config import firebaseConfig


firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
db = firebase.database()

app = Flask(__name__, template_folder='')
app.secret_key = uuid.uuid4().hex

month = ['Januari', 'Pebruari', 'Maret', 'April', 'Mei', 'Juni', 'Juli',
         'Agustus', 'September', 'Oktober', 'Nopember', 'Desember']


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('static/login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        all_users = db.child("admin").get()
        userlist = {}
        for user in all_users.each():
            userlist[user.key()] = user.val()

        for i, val in enumerate(userlist):
            if username == userlist[str(val)]['username']:
                if password == userlist[str(val)]['password']:
                    session['username'] = username
                    session['password'] = password

                    return redirect(url_for('dashboard'))

                else:
                    flash('password salah')

                    return render_template('static/login.html')

        flash('username tidak terdaftar')
        return render_template('static/login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    loginas = session['username']

    all_users = db.child("user").get()
    users = []

    for user in all_users.each():
        userls = list(user.val().values())
        users.append(userls)

    return render_template('static/dashboard.html', name=loginas, n_employs=len(users))


@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    DATE = ''
    d = ''
    m = ''
    y = ''
    loginas = session['username']

    if request.method == 'GET':
        day = datetime.now().day
        mon = datetime.now().month
        year = datetime.now().year

        d = str(day)
        m = month[int(mon)-1]
        y = str(year)

        if day < 10:
            sday = '0' + str(day)
        else:
            sday = str(day)

        if mon < 10:
            smon = '0' + str(mon)
        else:
            smon = str(mon)

        syear = str(year)

        DATE = syear + '-' + smon + '-' + sday

    if request.method == 'POST':
        date = request.form['date_input']
        d = str(int(date.split('-')[2]))
        m = month[int(int(date.split('-')[1]))-1]
        y = str(date.split('-')[0])

        DATE = date

    all_users = db.child("user").get()
    attend = []

    for user in all_users.each():
        id = user.val()['userid']
        att = db.child('attendance').child(id).child(y).child(m).child(d).child('at').get().val()
        ott = db.child('attendance').child(id).child(y).child(m).child(d).child('ot').get().val()
        if att is not None:
            if ott is not None:
                add = [user.val()['userid'], user.val()['username'], att, ott]
            else:
                add = [user.val()['userid'], user.val()['username'], att]
        else:
            add = [user.val()['userid'], user.val()['username']]

        attend.append(add)

    return render_template('static/attendance.html', name=loginas, result=attend, date_value=DATE)


@app.route('/userlist')
@login_required
def userlist():
    all_users = db.child("user").get()
    users = []

    for user in all_users.each():
        userls = list(user.val().values())
        users.append(userls)

    user = session['username']

    return render_template('static/userlist.html', name=user, result=users)


@app.route('/newuser', methods=['GET', 'POST'])
@login_required
def newuser():
    user = session['username']

    if request.method == 'POST':
        user_id = request.form['id']
        user_name = request.form['name']
        user_address = request.form['address']
        user_phone = request.form['phone']

        new_user = {
            "userid": user_id,
            "username": user_name,
            "useraddress": user_address,
            "userphone": user_phone
        }

        db.child('user').child(user_id).set(new_user)
        db.child("newuser").remove()

        return render_template('static/adduser.html', name=user)

    else:
        try:
            new_user = db.child("newuser").get().val()
            return render_template('static/adduser.html', name=user, rfid=new_user['id'])

        except:
            return render_template('static/adduser.html', name=user)


if __name__ == '__main__':
    app.run()
