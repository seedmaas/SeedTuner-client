import json
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from algorithm.binary_object import binary_object
from algorithm.client_solver import ClientSolver
from algorithm.Configs import bonline_task_config as btc

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
            executor = ThreadPoolExecutor(max_workers=self.coreNum/self.instance_length)
            # executor = ThreadPoolExecutor(max_workers=1)
        else:
            executor = ThreadPoolExecutor(max_workers=self.coreNum)
        all_task=[]
        try:
            for solver in self.solvers:
                self.detailDict[solver.binary_cmd]={}
                all_task.append(executor.submit(self.object_function, solver, scores,self.detailDict[solver.binary_cmd]))
            result = [i.result() for i in all_task]
            executor.shutdown()
            # print(scores)
            # print(self.solvers)
            # print(self.detailDict)
            self.update_scores(scores)
            # print(scores)
        except Exception as e:
            return 'error'

    def update_scores(self,scores):
        for index in range(len(scores)):
            self.scoreDict[self.solvers[index].binary_cmd]=scores[index]
        print(self.scoreDict)

def get_solvers_output(js):
    js = json.loads(js)
    task_id=js[0]['task_id']
    target=js[0]['target']
    single_cutoff=js[0]['single_cutoff']
    max_cores=js[0]['max_cores']
    cp=ClientProcess(task_id=task_id, target=target,
                     coreNum=max_cores,timeout=single_cutoff)
    cp.get_solvers(js)
    msg=cp.get_outputs()
    if msg != 'error':
        jfile=parse_to_jr(cp)
        data = json.loads(jfile)

        with open('output.json', 'w') as file:
        # 将数据写入文件
            json.dump(data, file)
        return parse_to_jr(cp)
    else:
        print("run error!!!!")
        jr={'msg':'error!!!!'}
        jr=json.dumps(jr)
        return jr

def parse_to_jr(cp):
    jr=[]
    for binary_cmd,score in cp.scoreDict.items():
        this_origin_cmd_info={}
        this_origin_cmd_info['origin_cmd']=binary_cmd
        this_origin_cmd_info['total_score']=score
        execute_cmds_info=[]
        for execute_cmd, output in cp.detailDict[binary_cmd].items():
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

if __name__=='__main__':
    js1='[{"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "0", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": "1"}]}, "origin_cmd": "python wrapper.py -seed 1 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd /home/zhouche && python a.py"}, {"execute_cmd_id": "1", "execute_cmd": "cd /home/zhouche && python a.py"}]}]' 
    get_solvers_output(js1)