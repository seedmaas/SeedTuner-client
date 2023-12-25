import json
import math
import multiprocessing
import os
import re
import subprocess
import sys
from algorithm.Configs import bonline_task_config as btc
import atexit
import os
import signal
import sys
import psutil

process=None 
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
        process.kill()
        
def terminate_task():
    global process
    kill(proc_pid=process.pid)

def pretest_running(js1):
    global process
    js1 = json.loads(js1)
    jr = {}
    if js1['target'] == 'MAX_TARGET':
        _abnormal_score = -1 * 1e9
    else:
        _abnormal_score = 1e9
    try:
        score = None
        process = subprocess.Popen(js1['default_cmd'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # proc = subprocess.run(js1['default_cmd'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        #                       timeout=math.ceil(1.2 * js1['single_cutoff']))
        # output = proc.stdout.decode()
        process.wait(timeout=math.ceil(1.2 * js1['single_cutoff']))
        output = process.stdout.read().decode()
        jr['msg'] = output
        pattern = r"<([^>]+)>"
        matches = re.findall(pattern, output)
        status = matches[0]
        score = float(matches[1])
        addition_rundata = matches[2]
        if status == 'SUCCESS':
            jr['res'] = 'true'
        else:
            jr['res'] = 'false'
    except Exception as e:
        jr['res'] = 'false'
        jr['msg'] = 'default cmd run error:'+str(e)
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr = json.dumps(jr, ensure_ascii=False)
    return jr


def get_instances_list(js1):
    js1 = json.loads(js1)
    jr = {}
    try:
        pwd=js1['instances_path']
        instances = os.listdir(js1['instances_path'])
        res_instances=[]
        for each in instances:
            each_instance=pwd+'/'+each
            res_instances.append(each_instance)
        btc.instance_length = len(res_instances)
        jr['instance_list'] = res_instances
    except Exception as e:
        jr['res'] = 'false'
        jr['msg'] = str(e)
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr['res'] = 'true'
    jr = json.dumps(jr, ensure_ascii=False)
    return jr


def get_max_cpu_cores():
    jr = {}
    try:
        max_core_num = multiprocessing.cpu_count()
        res = 'success'
        jr['max_core_num'] = max_core_num
        jr['res'] = res
    except Exception as e:
        jr['res'] = 'error'
        jr['msg'] = str(e)
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr = json.dumps(jr, ensure_ascii=False)
    return jr

if __name__ == '__main__':
    # js1 = '{"": "13","target": "MAX_TARGET","default_cmd": "python ../test.py","single_cutoff": 43}'
    # result = pretest_running(js1)
    # print(result)
    js1 = '{"instances_path":"~/test_client/instances"}'
    result = get_instances_list(js1)
    print(result)
