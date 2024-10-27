from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import RegistrationForm, LoginForm, RegistrationFormP, LoginFormP
import re , math
from datetime import datetime
import requests

app = Flask(__name__,template_folder='templates',static_folder='static')

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dummypwd'
app.config['MYSQL_DB'] = 'tapgenie'
mysql = MySQL(app)

@app.route("/")
def intro():
    return render_template('intro-page.html')

@app.route("/dashboard",methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
        account = cursor.fetchone()   
        return render_template('dashboard.html',account=account)
    return redirect(url_for('login'))
@app.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template('log-in-as-customer.html', form=form)

@app.route("/loginp",methods=['GET', 'POST'])
def loginP():
    form = LoginFormP() 
    if form.validate_on_submit():
        return redirect(url_for('appointment'))
    return render_template('log-in-as-professional.html', form=form)

@app.route("/signup",methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()   
    if request.method=='POST':
        if form.validate_on_submit():
            name = form.name.data
            mobile_no = form.phone_number.data
            email_ID = form.email.data
            password = form.password.data
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('INSERT INTO customer VALUES (% s, % s, % s, %s, DEFAULT, DEFAULT)', (name,mobile_no,email_ID,password))
            mysql.connection.commit()
            return redirect(url_for('login'))
    return render_template('create-account-as-customer.html',form=form)

@app.route("/signupp",methods=['GET', 'POST'])
def signupP():
    form = RegistrationFormP()
    if request.method=='POST':
        if form.validate_on_submit():
            name = form.name.data
            mobile_no = form.phone_number.data
            profession = form.profession.data
            email_ID = form.email.data
            password = form.password.data
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('INSERT INTO professional VALUES (% s, % s, % s,%s,%s, DEFAULT, DEFAULT)', (name, mobile_no, profession, email_ID, password))
            mysql.connection.commit()
            return redirect(url_for('loginP'))
    return render_template('create-account-as-professional.html',form=form)

@app.route("/appointment")
def appointment():
    if 'loggedin' in session:
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM appointments WHERE Professional_ID = % s AND appointment_date >= CURRENT_DATE()', (session['id'], ))
        active_bookings = cursor.fetchall()
        cursor.execute('SELECT * FROM appointments WHERE Professional_ID = % s AND appointment_date < CURRENT_DATE()', (session['id'], ))
        past_bookings = cursor.fetchall()
        return render_template('professional-template.html',active_bookings=active_bookings,past_bookings=past_bookings)
    return redirect(url_for('loginP'))

@app.template_filter('greatest_integer')
def gif(value):
    return math.floor(float(value))

@app.route("/bandw")
def bandw():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM service WHERE Service_category = "Beauty and Wellness"')
    services = cursor.fetchall()
    title = "BEAUTY AND WELLNESS"
    return render_template('appointment-template.html',services=services,title=title)

@app.route("/homec")
def homec():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM service WHERE Service_category = "Home Cleaning"')
    services = cursor.fetchall()
    title = "HOME CLEANING"
    return render_template('appointment-template.html',services=services,title=title)

@app.route("/apprep")
def apprep():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM service WHERE Service_category = "Appliance Repair"')
    services = cursor.fetchall()
    title = "APPLIANCE REPAIR"
    return render_template('appointment-template.html',services=services,title=title)

@app.route("/homerep")
def homerep():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM service WHERE Service_category = "Home Repair"')
    services = cursor.fetchall()
    title = "HOME REPAIR"
    return render_template('appointment-template.html',services=services,title=title)

@app.route("/paint")
def paint():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM service WHERE Service_category = "Home Painting"')
    services = cursor.fetchall()
    title = "HOME PAINTING"
    return render_template('appointment-template.html',services=services,title=title)

@app.route("/pest")
def pest():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM service WHERE Service_category = "Disinfection and Pest"')
    services = cursor.fetchall()
    title = "DISINFECTION AND PEST"
    return render_template('appointment-template.html',services=services,title=title)

@app.route("/index",methods=['GET', 'POST'])
def index2():
    msg = ''
    if 'loggedin' in session:
        service_id = request.args.get('id')
        category = service_category(service_id)
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM service WHERE Service_ID = %s',(service_id, ))
        service = cursor.fetchone()
        redirect_url = ""
        if category == "Beauty and Wellness": redirect_url = "bandw"
        elif category == "Home Cleaning": redirect_url = "homec"
        elif category == "Home Repair": redirect_url = "homerep"
        elif category == "Appliance Repair": redirect_url = "apprep"
        elif category == "Home Painting": redirect_url = "paint"
        elif category == "Disinfection and Pest": redirect_url = "pest"
        if request.method == 'POST' and 'datepicker' in request.form and 'color' in request.form:
            date = request.form['datepicker']
            slot = request.form['color']
            p = service['profession']
            # cursor.execute('SELECT * FROM professional')
            cursor.execute('SELECT pra.name, pra.mobile_no, pra.profession, pra.email_ID, pra.password, pra.professional_ID, pra.Rating FROM professional pra, appointments ap, service sr WHERE (((ap.appointment_date != %s OR ap.appointment_slot != %s) AND pra.profession = %s) AND (ap.professional_ID = pra.professional_ID)) UNION SELECT * FROM professional WHERE professional_ID NOT IN (SELECT Professional_ID FROM appointments) AND profession = %s',(date,slot,p,p))
            professionals = cursor.fetchall()
            return render_template('index-template.html', rurl = redirect_url,service = service,professionals=professionals,date=date,slot=slot)
        else:
            msg = 'Please fill out the form !'
            professionals={}
            date="2024-01-01"
            slot=1
            return render_template('index-template.html', rurl = redirect_url,service=service,professionals=professionals,date=date,slot=slot)
    return redirect(url_for('login'))
   
@app.template_filter('service_name')
def service_name(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT Service_name FROM service WHERE Service_ID = {id}')
    service = cursor.fetchone()
    return service['Service_name']

@app.route("/bookings",methods=['GET', 'POST'])
def bkc():
    if 'loggedin' in session:
        # if request.method == 'POST':
        #     text_rev = request.form['text_rev']
        #     # rate5 = request.form['rate-5']
        #     prof_id = request.args.get('id')
        #     cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
        #     cursor.execute('INSERT INTO review VALUES (DEFAULT, % s, % s, %s, %s,%s)', (3,prof_id,session['id'],text_rev,translate(text_rev)))
        #     mysql.connection.commit()
            # slot = request.form['color']
            # p = service['profession']


        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM appointments a JOIN professional p USING (professional_ID) WHERE a.customer_ID = %s AND a.appointment_date >= CURRENT_DATE()', (session['id'], ))
        active_bookings = cursor.fetchall()
        cursor.execute('SELECT * FROM appointments a JOIN professional p USING (professional_ID) WHERE a.customer_ID = %s AND a.appointment_date < CURRENT_DATE()', (session['id'], ))
        past_bookings = cursor.fetchall()
        return render_template('booking-template.html',active_bookings=active_bookings,past_bookings=past_bookings)
    return redirect(url_for('login'))

@app.route("/myprofile")
def mpc():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
        account = cursor.fetchone()   
        return render_template('my-profile-of-customer.html',account=account)
    return redirect(url_for('login'))
@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/logoutP")
def logoutP():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('loginP'))

@app.route("/update",methods=['GET', 'POST'])
def update():
    if 'loggedin' in session:
        if request.method == 'POST' and 'name' in request.form :
            name = request.form['name'] 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('UPDATE customer SET name =%s WHERE Customer_ID =% s', (name,session['id']))
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return render_template('my-profile-of-customer.html',account=account)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('name_update.html',account=account)
    else:

        return redirect(url_for('login'))
# def smth():

@app.route("/update2",methods=['GET', 'POST'])
def update2():
    if 'loggedin' in session:
        if request.method == 'POST' and 'number' in request.form :
            number = request.form['number'] 
            if len(number)==10:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                cursor.execute('UPDATE customer SET mobile_no =%s WHERE Customer_ID =% s', (number,session['id']))
            

                cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
                account = cursor.fetchone()
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template('my-profile-of-customer.html',account=account)
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
                account = cursor.fetchone()

                msg = 'Please enter valid phone number!'
                return render_template('phone_update.html', account=account)           
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('phone_update.html',account=account)
    else:

        return redirect(url_for('login'))

@app.route("/update_address",methods=['GET', 'POST'])
def update3():
    if 'loggedin' in session:
        if request.method == 'POST' and 'address' in request.form :
            name = request.form['address'] 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('UPDATE customer SET address =%s WHERE Customer_ID =% s', (name,session['id']))
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return render_template('my-profile-of-customer.html',account=account)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('address_update.html',account=account)
    else:

        return redirect(url_for('login'))

@app.route("/update4",methods=['GET', 'POST'])
def update4():
    if 'loggedin' in session:
        if request.method == 'POST' and 'password' in request.form :
            name = request.form['password'] 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('UPDATE customer SET password =%s WHERE Customer_ID =% s', (name,session['id']))
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return render_template('my-profile-of-customer.html',account=account)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE Customer_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('pw_update.html',account=account)
    else:

        return redirect(url_for('login'))


@app.route("/myprofile2")
def mpp():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM professional WHERE Professional_ID = % s', (session['id'], ))
        account = cursor.fetchone()   
        return render_template('my-profile-of-professional.html',account=account)
    return redirect(url_for('loginP'))

@app.route("/reviews")
def review():
    if 'loggedin' in session:
        date = request.args.get('date')
        slot = request.args.get('slot')
        sid = request.args.get('sid')
        pid = request.args.get('pid')
        pname =request.args.get('pname')
        lang =request.args.get('lang')
        # new = request.args.get('smth')
        # cid = session['id']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    

        cursor.execute('SELECT * FROM review JOIN customer USING (customer_ID) WHERE professional_ID = % s', (pid, ))
        revs = cursor.fetchall()
        category = service_category(sid)
        redirect_url = ""
        if category == "Beauty and Wellness": redirect_url = "bandw"
        elif category == "Home Cleaning": redirect_url = "homec"
        elif category == "Home Repair": redirect_url = "homerep"
        elif category == "Appliance Repair": redirect_url = "apprep"
        elif category == "Home Painting": redirect_url = "paint"
        elif category == "Disinfection and Pest": redirect_url = "pest"
        

    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM professional WHERE Professional_ID = % s', (session['id'], ))
    #     account = cursor.fetchone()   
        return render_template('reviews.html', rurl = redirect_url, sid = sid, pid = pid, date = date, slot = slot, revs = revs,pname=pname,lang=lang)
    return redirect(url_for('loginP'))

    
@app.route("/checkout",methods=['GET','POST'])
def ckc():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        date = request.args.get('date')
        slot = request.args.get('slot')
        sid = request.args.get('sid')
        pid = request.args.get('pid')
        new = request.args.get('smth')

        cursor.execute('SELECT * FROM service WHERE Service_ID = % s', (sid, ))
        serve = cursor.fetchone() 
        cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (pid, ))
        prof = cursor.fetchone()
        cursor.execute('SELECT Price FROM service WHERE Service_ID = % s', (sid, ))
        price = dict(cursor.fetchone())['Price']
        if request.method=="POST":
            if int(slot) == 1:
                stt = "09:00:00"
            elif int(slot)  == 2:
                stt = "12:00:00"
            elif int(slot)  == 3:
                stt = "15:00:00"
            else:
                stt = "18:00:00" 

            cursor.execute('INSERT INTO appointments VALUES (DEFAULT, % s, %s, %s, % s, % s, % s, %s)', (date, stt,new,session['id'],sid, pid, slot))
            mysql.connection.commit()
            return redirect(url_for('bkc'))
        return render_template('checkout.html',serve=serve,prof=prof,date=date,slot=slot)
    return redirect(url_for('login'))

@app.template_filter('service_category')
def service_category(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT Service_category FROM service WHERE Service_ID = {id}')
    service = cursor.fetchone()
    return service['Service_category']



@app.template_filter('pname')
def pname(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT name FROM professional WHERE professional_ID = {id}')
    prof = cursor.fetchone()
    return prof['name']

@app.template_filter('pmobile')
def pmobile(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT mobile_no FROM professional WHERE professional_ID = {id}')
    prof = cursor.fetchone()
    return prof['mobile_no']

@app.route("/details",methods=['GET','POST'])
def bkdc():
    if request.method == 'POST':
        text_rev = request.form['text_rev']
        
        prof_id = request.args.get('id')

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
        cursor.execute('INSERT INTO review VALUES (DEFAULT, % s, % s, %s, %s,%s)', (3,prof_id,session['id'],text_rev,(text_rev)))
        mysql.connection.commit()
        return redirect(url_for('bkc'))
        
        

    app_id = request.args.get('id')
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE appointment_ID = %s',(app_id, ))
    appointment = cursor.fetchone()
    return render_template('bkdc_template.html',appointment=appointment)
    # return redirect(url_for('bkc'))

@app.template_filter('cname')
def cname(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT name FROM customer WHERE Customer_ID = {id}')
    customer = cursor.fetchone()
    return customer['name']

@app.template_filter('cmobile')
def cmobile(id):
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f'SELECT mobile_no FROM customer WHERE Customer_ID = {id}')
    customer = cursor.fetchone()
    return customer['mobile_no']

@app.route("/details2")
def bkpd():
    app_id = request.args.get('id')
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE appointment_ID = %s',(app_id, ))
    appointment = cursor.fetchone()
    return render_template('bkpd_template.html',appointment=appointment)


@app.route("/updatep",methods=['GET', 'POST'])
def updateP():
    if 'loggedin' in session:
        if request.method == 'POST' and 'name' in request.form :
            name = request.form['name'] 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('UPDATE professional SET name =%s WHERE professional_ID =% s', (name,session['id']))
            cursor.execute('SELECT * FROM professional WHERE Professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return render_template('my-profile-of-professional.html',account=account)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM professional WHERE Professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('name_update_prof.html',account=account)
    else:

        return redirect(url_for('loginP'))

@app.route("/update2p",methods=['GET', 'POST'])
def update2P():
    if 'loggedin' in session:
        if request.method == 'POST' and 'number' in request.form :
            number = request.form['number'] 
            if len(number)==10:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                cursor.execute('UPDATE professional SET mobile_no =%s WHERE professional_ID =% s', (number,session['id']))
            

                cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
                account = cursor.fetchone()
                mysql.connection.commit()
                msg = 'You have successfully updated !'
                return render_template('my-profile-of-professional.html',account=account)
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
                account = cursor.fetchone()

                msg = 'Please enter valid phone number!'
                return render_template('phone_update_prof.html', account=account)           
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('phone_update_prof.html',account=account)
    else:

        return redirect(url_for('loginP'))

@app.route("/update_addressp",methods=['GET', 'POST'])
def update3P():
    if 'loggedin' in session:
        if request.method == 'POST' and 'address' in request.form :
            name = request.form['address'] 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('UPDATE professional SET profession =%s WHERE professional_ID =% s', (name,session['id']))
            cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return render_template('my-profile-of-professional.html',account=account)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('service_update_prof.html',account=account)
    else:

        return redirect(url_for('loginP'))

@app.route("/update4p",methods=['GET', 'POST'])
def update4P():
    if 'loggedin' in session:
        if request.method == 'POST' and 'password' in request.form :
            name = request.form['password'] 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)            
            cursor.execute('UPDATE professional SET password =%s WHERE professional_ID =% s', (name,session['id']))
            cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            mysql.connection.commit()
            msg = 'You have successfully updated !'
            return render_template('my-profile-of-professional.html',account=account)
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM professional WHERE professional_ID = % s', (session['id'], ))
            account = cursor.fetchone()
            msg = 'Please fill out the form !'
            return render_template('pw_update_prof.html',account=account)
    else:

        return redirect(url_for('loginP'))
def translate(qq):
   
    
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": qq,
        "target": "hi",
        "source": "en"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "a076b6bd15mshc96b2a003fbf3dcp143dbbjsn67d80a142f2e",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    return (response.json()['data']['translations'][0]['translatedText'])
   

if __name__ == '__main__':
    app.run(host = "0.0.0.0",debug=True)