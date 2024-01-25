import argparse
import json
import logging
import multiprocessing
import queue

import socketio

from algorithm import client_pretest
from algorithm import client_process
from algorithm.client_config import log_config

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description='A simple argument parser')
# 添加 name 参数，指定使用 -- 开头表示这是一个可选参数
parser.add_argument('--token', type=str, help='连接token')
parser.add_argument('--server', type=str, help='连接服务器')
# 解析命令行参数
args = parser.parse_args()
from algorithm import client_main

# 创建一个socketio客户端实例
sio = socketio.Client()
result_queue = queue.Queue()  # 用于存储 pretest_running 的结果
log_config.init_logger()
global current_running_total_solver
current_running_total_solver=None


@sio.on('get_cpu_cores')
def get_cpu_cores(emit_param_wrapper):
    logging.info('get_cpu_cores start with emit_param_wrapper:{}'.format(emit_param_wrapper))
    sio.emit('report_res', {
        'emit_id': emit_param_wrapper['emit_id'],
        'res': multiprocessing.cpu_count()
    })
    logging.info('get_cpu_cores end')


# 连接到服务器的函数
def connect_to_server():
    logging.info('Connecting to server...')
    # 连接到服务器，并在headers中发送token
    sio.connect(args.server, headers={'token': args.token})
    logging.info('Connected to server successfully with token: {}'.format(args.token))


@sio.on('get_instance_list')
def get_instance_list(emit_param_wrapper):
    logging.info('get_instance_list start with emit_param_wrapper:{}'.format(emit_param_wrapper))
    # js1 = '{"instances_path":"C:/Project/SeedTuner-client"}'
    result = client_pretest.get_instances_list(emit_param_wrapper["param"])
    sio.emit('report_res', {
        'emit_id': emit_param_wrapper['emit_id'],
        'res': result
    })
    logging.info('get_instance_res end')


@sio.on('pretest_running')
def pretest_running(emit_param_wrapper):
    logging.info('pretest_running start with emit_param_wrapper:{}'.format(emit_param_wrapper))
    emit_param = emit_param_wrapper["param"]
    client_main.init_task(emit_param)
    # js1 = '{"task_id": "111","target": "MAX_TARGET","default_cmd": "cd /home/zhouchen&&python a.py","single_cutoff": 9999}'
    result = client_pretest.pretest_running(emit_param)
    sio.emit('report_res', {
        'emit_id': emit_param_wrapper['emit_id'],
        'res': result
    })
    logging.info('pretest_running end')


@sio.on('terminate_task')
def terminate_task(param):
    global current_running_total_solver
    param = json.loads(param['param'])
    client_pretest.terminate_task(param['task_id'])
    if current_running_total_solver is not None:
        current_running_total_solver.kill()
        logging.info('done terminate:{}!'.format(param['task_id']))
        current_running_total_solver=None
    sio.emit('report_res', {
        'emit_id': param['emit_id'],
        'res': True
    })

@sio.on('run_task')
def pretest_running(emit_param_wrapper):
    global current_running_total_solver
    logging.info('run_task start with emit_param_wrapper:{}'.format(emit_param_wrapper))
    emit_param = emit_param_wrapper["param"]
    # emit_param = '[{"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "0", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": "1"}]}, "origin_cmd": "python wrapper.py -seed 1 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd /home/zhouchen && python a.py"}, {"execute_cmd_id": "1", "execute_cmd": "cd /home/zhouchen && python a.py"}]}]'
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=client_process.get_solvers_output, args=(emit_param, result_queue))
    current_running_total_solver=process
    process.start()

    # 阻塞，等待进程结束
    process.join()
    result = result_queue.get()

    # result = client_process.get_solvers_output(emit_param)
    sio.emit('report_res', {
        'emit_id': emit_param_wrapper['emit_id'],
        'res': result
    })
    logging.info('run task end')
    current_running_total_solver=None


if __name__ == '__main__':
    connect_to_server()
    sio.wait()  # 阻塞进程，直到客户端断开连接
