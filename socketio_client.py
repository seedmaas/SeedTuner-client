import socketio

from algorithm import client_pretest

# 创建一个socketio客户端实例
sio = socketio.Client()

# 这是一个示例token，实际使用时需要替换为有效的token
token = 'token1'


# 连接到服务器的函数
def connect_to_server():
    print('Connecting to server...')
    # 连接到服务器，并在headers中发送token
    sio.connect('http://39.106.153.79:8080', headers={'token': token})


@sio.on('get_instance_list')
def get_instance_list():
    print('get_instance_list start')
    js1 = '{"instances_path":"C:/Project/SeedTuner-client"}'
    result = client_pretest.get_instances_list(js1)
    sio.emit('get_instance_res', result)
    print('get_instance_res end')



@sio.on('pretest_running')
def pretest_running():
    print('pretest_running start')
    js1 = '{"task_id": "13","target": "MAX_TARGET","default_cmd": "python test.py","single_cutoff": 43}'
    result = client_pretest.pretest_running(js1)
    sio.emit('pretest_running_res', result)
    print('pretest_running end')


@sio.on('run_task')
def pretest_running():
    print('run_task start')
    js1 = '{"task_id": "13","target": "MAX_TARGET","default_cmd": "python test.py","single_cutoff": 43}'
    result = client_pretest.pretest_running(js1)
    sio.emit('get_running_res', result)
    print('pretest_running end')


if __name__ == '__main__':
    connect_to_server()
    sio.wait()  # 阻塞进程，直到客户端断开连接

# Note: To keep the connection alive, you should ensure that your Python script doesn't just exit.
# You may have to do something to keep it running, such as entering an infinite loop or waiting for user input.
