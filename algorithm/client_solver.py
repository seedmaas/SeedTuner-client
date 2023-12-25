import os
import subprocess
import re
import math
import threading
import algorithm.Logger.task_logging as logging



lock = threading.Lock()
class ClientSolver:
    def __init__(self,binary_cmd,final_execute_cmds,
                 target='MAX_TARGET',timeout=None):
        self.timeout = timeout
        self.binary_cmd = binary_cmd
        self.target=target
        self.cmd=None
        self.final_execute_cmds=final_execute_cmds

    def solve(self, task_id,performanceList,detail_list):
        lock.acquire()
        score=None
        for execute_cmd in self.final_execute_cmds:
            try:
                score=None
                proc = subprocess.run(execute_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        timeout=math.ceil(1.2 * self.timeout))
                output=proc.stdout.decode()
                pattern = r"<([^>]+)>"
                matches = re.findall(pattern, output)
                status=matches[0]
                if(matches[1]=='None'):
                    score=None
                else:
                    score = float(matches[1])
                addition_rundata=matches[2]
            except subprocess.TimeoutExpired:
                logging.logger.log(logging.Level.COMPULSORY, task_id, "", heads=["Algorithm", "TIME_OUT", "cmd: %s" % execute_cmd])
                performanceList.append(self._abnormal_score())
                detail_list[execute_cmd]='Result of this algorithm run:<%s>,<%s>,<%s>'% ('TIME_OUT',str(self._abnormal_score()),'None')
                lock.release()

            if score is None:
                logging.logger.log(logging.Level.COMPULSORY, task_id,
                                   "Auto-Tuner didn't find the algorithm score, please check the output!" ,
                                   heads=["Algorithm", "ERROR", "TIME_OUT", "cmd: %s" % execute_cmd])
                raise Exception("score not found! %s" % execute_cmd)
            else:
                logging.logger.log(logging.Level.COMPULSORY, task_id, "",
                                   heads=["Algorithm", "SUCCESS", "cmd: %s" % execute_cmd, "score:%s" % str(score)])
                performanceList.append(score)
                detail_list[execute_cmd]=output
        lock.release()

    def _abnormal_score(self):
        if self.target=='MAX_TARGET':
            return -1 * 1e9
        else:
            return 1e9

    def set_params(self, **params):
        if "timeout" in params:
            self.timeout = int(params["timeout"])
        if "max_object" in params:
            self.max_object = params["max_object"]
