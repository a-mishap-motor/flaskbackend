from flask import Flask,render_template,request,session,redirect
import os
from flask_socketio import SocketIO,emit,send,join_room,leave_room
from flask_mysqldb import MySQL
from flask_session import Session
app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'munlogindb'
mysql=MySQL(app)
socketio = SocketIO(app)
usar={}
lgcnt=0
@app.route('/',methods=['GET','POST'])
def test():
     if request.method=="POST":
         conn=mysql.connection.cursor()
         passw=request.form['password']
         user=request.form['username']
         conn.execute("SELECT * from logins where password=%s and username=%s",[passw,user])
         row=conn.fetchone()
         if row:
             #session['Username']=user
             #lgcnt +=1
             #if user=="aditya":
                 #return render_template('index.html')
             #else:
             return render_template('testindex.html')
             #print("user logged in" + request.sid)
         else:
             #return render_template("")

             return "Username and/or password incorrect."

         #return request.form['username'] + " logged in"
     return render_template("login.html")
#@socketio.on('message')
#def handlemessage(msg):
    #print("Message:" + msg)
    #send(msg,broadcast=True)
#@socketio.on('connect')
#def test_connect():
    #emit('my response', {'data': 'Connected'})
    #print("connected to user is" + request.sid)

@socketio.on('connect')
def test_connect():
    #emit('my response', {'data': 'Connected'})
    print("")
@socketio.on('roomc')
def showroomconnect():
    print("Sid here" + request.sid)
@socketio.on('connect',namespace="/reg")
def hello():
    print('')#'User:' + 'msg' + ' request:' + request.sid)

@socketio.on('regi',namespace="/reg")
def registeruser(user):
    #print('User:' + msg + ' request:' + request.sid)
    usar[user]=request.sid
    print("registered user:" + user +"with sid:" +usar[user])

@socketio.on('sendmess')
def send(obj):
    recip=obj['rece']
    sendsid=usar[obj['rece']]
    mess=obj['message']
    print('User:' + recip + ' msg:' + mess + 'sid' + sendsid)
    emit('new_message',mess,room=sendsid)

@socketio.on('GetOthers',namespace='/reg')
def senduserlist(usur):
    #print("Get others,registered user:" + usur +"with sid:" +request.sid)
    key=list(usar.keys())
    l=len(key)
    payload={'key':key,'len':l}
    emit('GetUserList',payload,broadcast=True)

if __name__=="__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
