import json
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from binary_object import binary_object
from client_solver import ClientSolver
from Configs import bonline_task_config as btc

class ClientProcess:
    def __init__(self,task_id,target,coreNum,timeout):
        self.object_function = partial(binary_object, task_id=task_id, target=target)
        self.coreNum=coreNum
        self.solvers=[]
        self.scoreDict={}
        self.target=target
        self.timeout=timeout
        self.detailDict={}
        self.instance_length=btc.instance_length

    def get_solvers(self,js):
        for solver_data in js:
            origin_cmd_id=solver_data['origin_cmd_id']
            binary_cmd=solver_data['origin_cmd']
            execute_cmds_data=solver_data['execute_cmds']
            final_execute_cmds=[]
            for execute_cmd_data in execute_cmds_data:
                final_execute_cmds.append(execute_cmd_data['execute_cmd'])
            cs=ClientSolver(binary_cmd=binary_cmd,final_execute_cmds=final_execute_cmds,target=self.target,timeout=self.timeout)
            self.solvers.append(cs)

    def get_outputs(self):
        if self.solvers==None:
            return 'ERROR'
        scores=[]
        if self.instance_length!=0:
            executor = ThreadPoolExecutor(max_workers=self.coreNum/len(self.instance_length))
        else:
            executor = ThreadPoolExecutor(max_workers=self.coreNum)
        all_task=[]
        for solver in self.solvers:
            all_task.append(executor.submit(self.object_function, solver, scores,self.detailDict))
        result = [i.result() for i in all_task]
        executor.shutdown()
        self.update_scores(scores)
        print(scores)

    def update_scores(self,scores):
        for index in range(len(scores)):
            self.scoreDict[self.solvers[index].binary_name]=scores[index]
        print(self.scoreDict)

def get_solvers_output(js):
    js = json.loads(js)
    task_id=js['task_id']
    target=js['target']
    single_cutoff=js['single_cutoff']
    max_cores=js['max_cores']
    cp=ClientProcess(task_id=task_id, target=target,
                     coreNum=max_cores,timeout=single_cutoff)
    cp.get_solvers(js)
    cp.get_outputs()
    return parse_to_jr(cp)

def parse_to_jr(cp):
    jr=[]
    for binary_cmd,score in cp.detailDict.items():
        this_origin_cmd_info={}
        this_origin_cmd_info['origin_cmd']=binary_cmd
        this_origin_cmd_info['total_score']=score
        execute_cmds_info=[]
        for execute_cmd, output in cp.detailDict.items():
            execute_cmd_info={}
            pattern = r"<([^>]+)>"
            matches = re.findall(pattern, output)
            status = matches[0]
            score = float(matches[1])
            addition_rundata = matches[2]
            execute_cmd_info['execute_cmd']=execute_cmd
            execute_cmd_info['execute_cmd_score']=score
            execute_cmd_info['execute_cmd_status']=status
            execute_cmds_info.append(execute_cmd_info)
        this_origin_cmd_info['execute_cmds']=execute_cmds_info
        jr.append(this_origin_cmd_info)
    jr=json.dumps(jr)
    return jr
