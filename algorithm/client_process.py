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
    cp.get_outputs()
    jfile=parse_to_jr(cp)
    data = json.loads(jfile)

    with open('output.json', 'w') as file:
    # 将数据写入文件
        json.dump(data, file)
    return parse_to_jr(cp)

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
    js1='[{"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "0", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": "1"}]}, "origin_cmd": "python wrapper.py -seed 1 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 1 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 1 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 1 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 1 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 1 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "1", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 417}]}, "origin_cmd": "python wrapper.py -seed 417 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 417 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 417 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 417 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 417 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 417 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "2", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 988}]}, "origin_cmd": "python wrapper.py -seed 988 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 988 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 988 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 988 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 988 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 988 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "3", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 0}]}, "origin_cmd": "python wrapper.py -seed 0 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 0 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 0 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 0 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 0 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 0 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "4", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 699}]}, "origin_cmd": "python wrapper.py -seed 699 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 699 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 699 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 699 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 699 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 699 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "5", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 211}]}, "origin_cmd": "python wrapper.py -seed 211 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 211 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 211 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 211 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 211 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 211 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "6", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 558}]}, "origin_cmd": "python wrapper.py -seed 558 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 558 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 558 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 558 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 558 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 558 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "7", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 834}]}, "origin_cmd": "python wrapper.py -seed 834 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 834 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 834 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 834 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 834 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 834 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "8", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 103}]}, "origin_cmd": "python wrapper.py -seed 103 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 103 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 103 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 103 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 103 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 103 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "9", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 313}]}, "origin_cmd": "python wrapper.py -seed 313 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 313 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 313 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 313 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 313 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 313 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}, {"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "10", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": 908}]}, "origin_cmd": "python wrapper.py -seed 908 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 908 -instance ~/test_client/instances/true.cnf -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 908 -instance ~/test_client/instances/bin1.cnf -cutoff_time 40 "}, {"execute_cmd_id": "2", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 908 -instance ~/test_client/instances/bin2.cnf -cutoff_time 40 "}, {"execute_cmd_id": "3", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 908 -instance ~/test_client/instances/bin3.cnf -cutoff_time 40 "}, {"execute_cmd_id": "4", "execute_cmd": "cd ~/test_client/PbO-CCSAT-master/PbO-CCSAT_object_oriented_version_source_code &&python wrapper.py -seed 908 -instance ~/test_client/instances/eq1.cnf -cutoff_time 40 "}]}]' 
    get_solvers_output(js1)