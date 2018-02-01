from flask import Flask,render_template,request,session,redirect
import os
from flask_socketio import SocketIO,emit
from flask_mysqldb import MySQL
app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'munlogindb'
mysql=MySQL(app)
socketio = SocketIO(app)
@app.route('/',methods=['GET','POST'])
def test():
     if request.method=="POST":
         conn=mysql.connection.cursor()
         passw=request.form['password']
         user=request.form['username']
         conn.execute("SELECT * from logins where password=%s and username=%s",[passw,user])
         row=conn.fetchone()
         if row:
             session['Username']=user
             return render_template("index.html")
         else:
             #return render_template("")
             return "Username and/or password incorrect."

         #return request.form['username'] + " logged in"
     return render_template("login.html")
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})
if __name__=="__main__":
    socketio.run(app)
