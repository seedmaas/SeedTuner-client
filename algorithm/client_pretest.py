import json
import math
import multiprocessing
import os
import re
import subprocess

from algorithm.Configs import bonline_task_config as btc


def pretest_running(js):
    js = json.loads(js)
    jr = {}
    if js['target'] == 'MAX_TARGET':
        _abnormal_score = -1 * 1e9
    else:
        _abnormal_score = 1e9
    try:
        score = None
        proc = subprocess.run(js['default_cmd'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              timeout=math.ceil(1.2 * js['single_cutoff']))
        output = proc.stdout.decode()
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
        jr['msg'] = str(e)
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr = json.dumps(jr, ensure_ascii=False)
    return jr


def get_instances_list(js1):
    js1 = json.loads(js1)
    jr = {}
    try:
        instances = os.listdir(js1['instances_path'])
        btc.instance_length = len(instances)
        jr['instance_list'] = instances
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


'''
test1

'''

'''
test2

print()
'''

if __name__ == '__main__':
    # js1 = '{"": "13","target": "MAX_TARGET","default_cmd": "python ../test.py","single_cutoff": 43}'
    # result = pretest_running(js1)
    # print(result)
    js1 = '{"instances_path":"/Users/kevinzc9"}'
    result = get_instances_list(js1)
    print(result)
