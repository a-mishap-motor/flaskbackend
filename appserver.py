from flask import Flask,render_template
from flask_socketio import SocketIO,emit
app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
@app.route('/')
def test():
    return render_template("login.html")
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})
if __name__=="__main__":
    socketio.run(app)




