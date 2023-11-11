import socketio

sio = socketio.Client()

token = 'token1'  # 假设你已经有了一个有效的token


@sio.on('connect')
def on_connect():
    print('Connected to server with token {}'.format(token))


@sio.on('response_cpu_count')
def on_request_cpu_count():
    cpu_count = get_cpu_count()  # 假设你有一个函数可以获取CPU数量
    print('CPU count requested, responding with count:', cpu_count)

    # 发送CPU数量给服务器
    sio.emit('response_cpu_count', {'id': token, 'count': cpu_count})


@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from server')


def get_cpu_count():
    import multiprocessing
    return multiprocessing.cpu_count()  # 获取CPU数量的方法


def connect_to_server():
    print('Connecting to server...')
    sio.connect('http://localhost:5000', headers={'token': token})


if __name__ == '__main__':
    connect_to_server()
    on_request_cpu_count()
    sio.wait()  # 阻塞进程，直到客户端断开连接



# Note: To keep the connection alive, you should ensure that your Python script doesn't just exit.
# You may have to do something to keep it running, such as entering an infinite loop or waiting for user input.
