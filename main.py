from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = '_sbDdEOVwmMzzbn7eROWxg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'newdb'
mysql = MySQL(app)

@app.route('/')
def yesss():
        return "hello world"

@app.route('/main11', methods=['GET', 'POST'])
def login():
        if 'username' in session:
            username = session['username']
            if session['username'] != "admin":
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT COUNT(*) FROM devices WHERE user_id=%s", (session['id'],))
                property_count = cursor.fetchall()
                return render_template("index.html", user=session['username'],count=property_count)
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT COUNT(*) FROM users")
                property_count = cursor.fetchall()
                return render_template("index11.html", count=property_count)
        elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
                username1 = request.form['username']
                password1 = request.form['password']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username1, password1))
                account = cursor.fetchone()
                if account['username']=="admin":
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    cursor.execute("SELECT COUNT(*) FROM users")
                    property_count = cursor.fetchall()
                    return render_template("index11.html", count=property_count)
                elif account['username'] != "admin":
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    cursor.execute("SELECT COUNT(*) FROM devices WHERE user_id=%s", (account['id'],))
                    property_count = cursor.fetchall()
                    return render_template("index.html", user=session['username'], count=property_count)
                else:
                    msg = 'Incorrect username/password!'
                    return "Page did not load"
        else:
            return render_template("page-login.html")

@app.route("/insertredir")
def ins1():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM home_devices WHERE user_id=%s", (session['id'],))
    result = cursor.fetchall()
    return render_template("add_device.html", len=len(result), print=result)

@app.route('/addrules')
def hdform():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM devices WHERE user_id=%s",(session['id'],))
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM home_devices WHERE user_id=%s", (session['id'],))
    result1 = cursor.fetchall()
    return render_template("add_rules.html", string2=result, len=len(result), string3=result1, len1=len(result1))

@app.route('/manageusers')
def viewu():
    if session["username"] == "admin":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
        result1 = cursor.fetchall()
        return render_template("view_users.html", result1 = result1, len=len(result1))
    else:
        return "You are not admin"

@app.route('/addrulestodb', methods = ['GET','POST'])
def artdb():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    fvariable = request.form['device']
    svariable = request.form['appl']
    con = request.form['con']
    cursor.execute("SELECT * FROM devices WHERE device=%s",(fvariable,))
    r1 = cursor.fetchall()
    cursor.execute("SELECT * FROM home_devices WHERE dname=%s",(svariable,))
    r2 = cursor.fetchall()
    r11 = r1[0]['id']
    r22 = r2[0]['id']
    cursor.execute("INSERT INTO conditions(`user_id`, `imid`, `amid`, `condition`) VALUES(%s, %s, %s, %s)", (session['id'], r11, r22, con))
    mysql.connection.commit()
    return redirect(url_for('viewr'))

@app.route('/homedevice', methods = ['GET','POST'])
def ahd():
    if request.method == 'POST' and 'hdevice' in request.form:
        hdevice = request.form['hdevice']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO `home_devices`(`user_id`, `dname`) VALUES (%s, %s)", (session['id'], hdevice))
        return redirect(url_for('viewd'))

@app.route("/view")
def viewd():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM devices WHERE user_id=%s", (session['id'],))
    result = cursor.fetchall()
    return render_template("view_device.html", len=len(result), string1=result, user=session['username'])

@app.route('/insert', methods = ['GET','POST'])
def ins():
    if request.method == 'POST' and 'device' in request.form and 'ip' in request.form:
        device = request.form['device']
        ip = request.form['ip']
        mac = request.form['mac']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO `devices`(`user_id`, `device`, `mac`, `ip`) VALUES (%s, %s, %s, %s)", (session['id'], device, mac, ip))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('viewd'))
    else:
        return str(session['id'])

@app.route('/edit/<int:editid>')
def ed(editid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM `devices` WHERE `id`=%s" %editid,)
    resultedit = cursor.fetchall()
    return render_template("edit.html", newvalue=resultedit)

@app.route('/update/<int:editid1>', methods = ['GET','POST'])
def up(editid1):
    device = request.form['device']
    ip = request.form['ip']
    mac  = request.form['mac']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE  `devices`  SET  `device` = %s, `mac` = %s, `ip` = %s  WHERE  `id` = %s", (device, mac, ip, editid1))
    mysql.connection.commit()
    return redirect(url_for('viewd'))

@app.route('/delete/<int:delid>')
def delete(delid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM `devices` WHERE id=%s" %delid)
    return redirect(url_for('viewd'))

@app.route('/viewrules')
def viewr():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select conditions.id, devices.device, home_devices.dname, conditions.condition from conditions "
                   "INNER JOIN devices on conditions.imid = devices.id INNER JOIN home_devices on conditions.amid = "
                   "home_devices.id WHERE devices.user_id=%s;", (session['id'],))
    result = cursor.fetchall()
    return render_template("view_rules.html", result = result, len = len(result))

@app.route('/ruleupview/<int:editid>', methods = ['GET','POST'])
def ruleup(editid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM devices WHERE user_id=%s", (session['id'],))
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM home_devices WHERE user_id=%s", (session['id'],))
    result1 = cursor.fetchall()
    cursor.execute("SELECT * FROM conditions WHERE id=%s" %editid)
    result2 = cursor.fetchall()
    return render_template("edit_rules.html", result=result, len=len(result), result1=result1, len1=len(result1), result2=result2, len2=len(result2))

@app.route('/updaterules/<int:editid1>', methods = ['GET','POST'])
def uprules(editid1):
    device = request.form['device']
    appl = request.form['appl']
    con = request.form['con']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM devices WHERE device=%s", (device,))
    r1 = cursor.fetchall()
    cursor.execute("SELECT * FROM home_devices WHERE dname=%s", (appl,))
    r2 = cursor.fetchall()
    r11 = r1[0]['id']
    r22 = r2[0]['id']
    cursor.execute("UPDATE  `conditions`  SET  `user_id` = %s, `imid` = %s, `amid` = %s, `condition` = %s  WHERE  `id` = %s", (session['id'], r11, r22, con, editid1))
    mysql.connection.commit()
    return redirect(url_for('viewr'))

@app.route('/delrule/<int:delid>')
def delr(delid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM `conditions` WHERE id=%s" % delid)
    return redirect(url_for('viewr'))
@app.route('/login/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

#################################################################admin panel#################################################################
@app.route('/adminedit/<int:editid>')
def aedit(editid):
    if session['username'] == "admin":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM `users` WHERE `id`=%s" % editid, )
        resultedit = cursor.fetchall()
        return render_template("admin_edit.html", newvalue=resultedit)
    else:
        return render_template("page-error-403.html")

@app.route('/adminupdate/<int:editid>', methods = ['GET','POST'])
def aupdate(editid):
    if session['username'] == "admin":
        username = request.form['username']
        email = request.form['email']
        password  = request.form['password']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        device_id = request.form['device_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE  `users`  SET  `username` = %s, `email` = %s, `password` = %s,  `birthdate` = %s, `gender` = %s, `device_id` = %s WHERE  `id` = %s", (username, email, password, birthdate, gender, device_id, editid))
        mysql.connection.commit()
        return redirect(url_for('viewu'))
    else:
        return render_template("page-error-403.html")

@app.route('/adminadduser1', methods=['GET', 'POST'])
def adadd1():
    if session['username'] == "admin":
        return render_template("admin_add_user.html")
    else:
        return render_template("page-error-403.html")

@app.route('/adminadduser2', methods = ['GET','POST'])
def adadd2():
    if session['username'] == 'admin':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        device_id = request.form['device_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO `users`(`username`, `email`, `password`, `birthdate`, `gender`, `device_id`) VALUES (%s, %s, %s, %s, %s, %s)",(username, email, password, birthdate, gender, device_id,))
        mysql.connection.commit()
        return redirect(url_for('viewu'))
    else:
        return render_template("page-error-403.html")

@app.route('/admindelete/<int:delid>')
def adelete(delid):
    if session['username'] == "admin":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM `users` WHERE id=%s" % delid)
        return redirect(url_for('viewu'))
    else:
        return render_template("page-error-403.html")
#################################################################admin panel over#################################################################

if __name__ == '__main__':
    app.run(debug = True)
