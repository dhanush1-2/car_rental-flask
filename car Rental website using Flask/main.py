from flask import Flask , render_template ,request, redirect, url_for, session,flash
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car_rent'


mysql = MySQL(app)


# start page route
@app.route('/')
def index():
    return render_template('UserLogin.html')
#home page route
@app.route('/home')
def home():
    return render_template('rental.html',username=session['username'])
#User Sign up route
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        userdetails = request.form
        txt = userdetails['name']
        email = userdetails['email']
        pswd = userdetails['password']
        number = userdetails['number']
        address = userdetails['address']
        country = userdetails['country']
        city = userdetails['city']
        dob = userdetails['dob']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tblusers(FullName, EmailId, Password, ContactNo, dob, Address, City, Country) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (txt,email,pswd,number,dob,address,city,country))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('signup.html')
#User login Route
@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pswd']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tblusers WHERE EmailId=%s AND Password=%s',(username,password))
        record=cur.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[2]
            flash('logged in successfully')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password')
    return render_template('UserLogin.html',msg=msg)
#User logout Route
@app.route('/logout')
def logoutuser():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('userlogin'))

#Vehicle Booking Routes

@app.route('/booking',methods=['GET','POST'])
def booking():
    if request.method == 'POST':
        vehidetails = request.form
        strtdate = vehidetails['strtdate']
        enddate = vehidetails['enddate']
        mail=session['username']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tblbooking(userEmail,VehicleId,FromDate,ToDate,Status) values(%s,%s,%s,%s,%s)" , (mail,"1",strtdate,enddate,"CONFIRMED",))
        mysql.connection.commit()
        cur.close()        
        return redirect(url_for('home'))
    return render_template('carbook1.html')

# 2nd vehicle booking
@app.route('/booking1',methods=['GET','POST'])
def booking1():
    if request.method == 'POST':
        vehidetails = request.form
        strtdate = vehidetails['strtdate']
        enddate = vehidetails['enddate']
        mail=session['username']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tblbooking(userEmail,VehicleId,FromDate,ToDate,Status) values(%s,%s,%s,%s,%s)" , (mail,"2",strtdate,enddate,"CONFIRMED",))
        mysql.connection.commit()
        cur.close()        
        return redirect(url_for('home'))
    return render_template('carbook2.html')


# 3rd vehicle booking
@app.route('/booking2',methods=['GET','POST'])
def booking2():
    if request.method == 'POST':
        vehidetails = request.form
        strtdate = vehidetails['strtdate']
        enddate = vehidetails['enddate']
        mail=session['username']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tblbooking(userEmail,VehicleId,FromDate,ToDate,Status) values(%s,%s,%s,%s,%s)" , (mail,"3",strtdate,enddate,"CONFIRMED",))
        mysql.connection.commit()
        cur.close()        
        return redirect(url_for('home'))
    return render_template('carbook3.html')



#Admin login Route
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    msg1=''
    if request.method == 'POST':
        username1 = request.form['ausername']
        password1 = request.form['apswd']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE UserName=%s AND Password=%s',(username1,password1))
        record=cur.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[2]
            flash('logged in successfully')
            return redirect(url_for('users'))
        else:
            flash('Incorrect username or password')
    return render_template('Admin login.html',msg=msg1)
#Admin Logout Route
@app.route('/logouta')
def logoutadmin():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('adminlogin'))

#User details in dashboard
@app.route('/users',methods=['GET','POST'])
def users():
    cur = mysql.connection.cursor()
    cur.execute('Select id,FullName,EmailId,ContactNo,dob,Address,City,Country from tblusers ')
    data = cur.fetchall()
    return render_template("indexusers.html",value=data)

#Vehicle  details in dashboard
@app.route('/vehicledetails',methods=['GET','POST'])
def vehicledetails():
    cur = mysql.connection.cursor()
    cur.execute('Select * from tblvehicles')
    data = cur.fetchall()   
    if request.method == 'POST':
        vehicledetails = request.form
        name1 = vehicledetails['vname']
        brand = vehicledetails['vbrand']
        overview = vehicledetails['voverview']
        price = vehicledetails['vprice']
        fuel = vehicledetails['vfueltype']
        model = vehicledetails['vmodelyear']
        cur.execute("INSERT INTO tblvehicles(VehiclesTitle,Vehiclesbrand, VehiclesOverview, PricePerDay, FuelType, ModelYear) VALUES(%s,%s,%s,%s,%s,%s)", (name1,brand,overview,price,fuel,model))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('dash'))
    return render_template("indexvehicles.html",value=data)



#user view bookings
@app.route('/uservehidetails',methods=['GET','POST'])
def uservehidetails():
    cur = mysql.connection.cursor()
    cur.execute('Select b.id,b.userEmail,v.VehiclesTitle,v.VehiclesBrand,v.PricePerDay,b.FromDate,b.ToDate,b.Status from tblbooking b,  tblvehicles v where b.VehicleId = v.Id and b.userEmail=%s',(session['username'],))
    data = cur.fetchall()
    return render_template("uservehicledetails.html",value=data)

#cancel booking
@app.route('/cancel/<string:id_data>',methods=['GET'])
def cancel(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()    
    cur.execute('Delete from tblbooking where id=%s ',(id_data,))    
    mysql.connection.commit() 
    return redirect(url_for('booking'))

#delete vehicles
@app.route('/delete/<string:idata>',methods=['GET'])
def delete(idata):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute('Delete from tblvehicles where VehiclesTitle=%s',(idata,))
    mysql.connection.commit() 
    return redirect(url_for('dash'))



#Booking details
@app.route('/bookingdetails',methods=['GET','POST'])
def bookingdetails():
    cur = mysql.connection.cursor()
    cur.execute('Select * from tblbooking')
    data = cur.fetchall()
    return render_template("indexbookings.html",value=data)




if __name__ == '__main__':
    app.run(debug=True)