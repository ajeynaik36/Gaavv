from flask import Flask,redirect,url_for,render_template, request,session
import pymysql
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

con = pymysql.connect("localhost", "root", "", "gaavv")
cur = con.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/a')
def a():
    return render_template('signup.html')


@app.route('/b')
def b():
    return render_template('signin.html')


@app.route('/c')
def c():
    return render_template('contact.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/read ', methods=["GET", "POST"])
def read():
    if request.method == "POST":

        uname = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        gender = request.form.get("gender")
        number = request.form.get("number")

        try:
            q = "insert into register(uname,pass,email,gender,nunber) values('{}','{}','{}','{}','{}')".format(uname, password,email,gender,number)
            cur.execute(q)
            return render_template('fleet.html')

        except pymysql.err.IntegrityError:
            return render_template('already.html')
        except:
            return render_template('failure.html')


@app.route('/login ', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("name")
        password = request.form.get("pass")
        if email == "admin" and password == "password":
            return render_template('admin.html')
        else:
            q = "select * from register where email='{}' and pass='{}'".format(email, password)
            cur.execute(q)
            res = cur.fetchall()
            if len(res) >= 1:
                session['email'] = email
                session['password'] = password
                return render_template("fleet.html")
            else:
                return render_template('failurelogin.html')


@app.route('/book')
def book():
    q = "select * from fleet"

    cur.execute(q)
    res = cur.fetchall()
    if len(res) > 0:
        return render_template('book.html', names=res,)
    else:
        return render_template('novehicle.html')


@app.route('/remv', methods=["Get","POST"])
def remv():
    if request.method == "POST":
        name = request.form.get("name")
        no = request.form.get("no")
        q = "delete from fleet where name='{}' and phone='{}'".format(name,no)
        cur.execute(q)
        return render_template('remsuccess.html')

@app.route('/dash')
def dash():

    q = "select * from fleet"
    cur.execute(q)
    res = cur.fetchall()
    return render_template('dash.html',names=res)



@app.route('/z ')
def z():
    session.clear()
    return render_template('logout.html')


@app.route('/add')
def add():
    return render_template('addvehicle.html')


@app.route('/remove')
def remove():
    return render_template('remove.html')


@app.route('/addv',methods= ["POST"])
def addv():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        vno = request.form.get("vno")
        vtype = request.form.get("type")
        cap = request.form.get("cap")
        lug = request.form.get("lug")
        phone = request.form.get("no")
        try:
            q = "insert into fleet(name, adress, vno, type, capacity, luggage, phone) values('{}','{}','{}','{}','{}','{}','{}')".format(name, address, vno, vtype, cap, lug, phone)
            cur.execute(q)
            return render_template('addedsuccess.html')
        except pymysql.err.IntegrityError:
            return render_template('alreadyveh.html')


if __name__ == "__main__":
    app.run(debug = True,port = 4555)
