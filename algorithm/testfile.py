import sys
import os

project_root = "/home/zhouchen/test_client/SeedTuner-client"  # 替换为服务器项目的根目录
sys.path.append(project_root)
from algorithm import client_process

# emit_param = '[{"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "0", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": "1"}]}, "origin_cmd": "python wrapper.py -seed 1 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd /home/zhouchen && python a.py"}, {"execute_cmd_id": "1", "execute_cmd": "cd /home/zhouchen && python a.py"}]}]'
emit_param=' [{"task_id": "222", "target": "MAX_TARGET", "single_cutoff": 3000, "max_cores": 3, "origin_cmd_id": "0", "params": {"fixed_params": [{"name": "a", "value": "100"}], "tuned_params": [{"name": "b", "value": -597}, {"name": "c", "value": -438}, {"name": "d", "value": "true"}, {"name": "e", "value": "true"}]}, "origin_cmd": "python wrapper.py -a 100 -b -284 -c 397 -d false -e true ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd /home/zhouchen/alg &&python wrapper.py -a 100 -b -284 -c 397 -d false -e true -instance /home/zhouchen/alg/instances/instance1.txt -cutoff_time 40 "}, {"execute_cmd_id": "1", "execute_cmd": "cd /home/zhouchen/alg &&python wrapper.py -a 100 -b -284 -c 397 -d false -e true -instance /home/zhouchen/alg/instances/instance2.txt -cutoff_time 40 "}]}]'
result = client_process.get_solvers_output(emit_param)
print(result)