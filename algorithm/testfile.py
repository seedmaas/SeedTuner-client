from algorithm import client_process

emit_param = '[{"task_id": "111", "target": "MAX_TARGET", "single_cutoff": 100, "max_cores": 3, "origin_cmd_id": "0", "params": {"fixed_params": [], "tuned_params": [{"name": "seed", "value": "1"}]}, "origin_cmd": "python wrapper.py -seed 1 ", "execute_cmds": [{"execute_cmd_id": "0", "execute_cmd": "cd /home/zhouchen && python a.py"}, {"execute_cmd_id": "1", "execute_cmd": "cd /home/zhouchen && python a.py"}]}]'
result = client_process.get_solvers_output(emit_param)
