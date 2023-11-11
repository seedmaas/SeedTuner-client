import socketio

# 创建一个Socket.IO客户端
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('my_event', {'data': 'I\'m connected!'})

@sio.event
def my_response(data):
    print('Received message: ', data)

@sio.event
def disconnect():
    print('I\'m disconnected')

# Connect to the server
sio.connect('http://localhost:5000')

# Keep the app running
sio.wait()
