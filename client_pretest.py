import json
import math
import os
import re
import subprocess
import multiprocessing
from Configs import bonline_task_config as btc

def pretest_running(js):
    js = json.loads(js)
    jr = {}
    if js['target']=='MAX_TARGET':
        _abnormal_score= -1 * 1e9
    else:
        _abnormal_score= 1e9
    try:
        score = None
        proc = subprocess.run(js['default_cmd'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              timeout=math.ceil(1.2 * js['single_cutoff']))
        output = proc.stdout.decode()
        jr['output'] = output
        pattern = r"<([^>]+)>"
        matches = re.findall(pattern, output)
        status = matches[0]
        score = float(matches[1])
        addition_rundata = matches[2]
        if status=='SUCCESS':
            jr['res']='success'
        else:
            jr['res']='error'
    except subprocess.TimeoutExpired:
        jr['res'] = 'success'
        jr['output'] ='Result of this algorithm run:<%s>,<%s>,<%s>' % (
        'TIME_OUT', str(_abnormal_score), 'None')
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr = json.dumps(jr, ensure_ascii=False)
    return jr

def get_instances_list(js):
    js = json.loads(js)
    jr = {}
    try:
        instances=os.listdir(js['instances_path'])
        btc.instance_length=len(instances)
        jr['instances_path']=instances
    except Exception as e:
        jr['res'] = 'error'
        jr['msg'] = str(e)
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr['res']='success'
    jr = json.dumps(jr,ensure_ascii=False)
    return jr

def get_max_cpu_cores():
    jr={}
    try:
        max_core_num = multiprocessing.cpu_count()
        res='success'
        jr['max_core_num']=max_core_num
        jr['res']=res
    except Exception as e:
        jr['res']='error'
        jr['msg']=str(e)
        jr = json.dumps(jr, ensure_ascii=False)
        return jr
    jr = json.dumps(jr,ensure_ascii=False)
    return jr
