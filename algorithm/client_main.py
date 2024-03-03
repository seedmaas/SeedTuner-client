import algorithm.Logger.task_logging as logging
import os
import json
from algorithm.Configs import bonline_task_config as btc

def init_task(js1):
    js1 = json.loads(js1)
    task_id=js1['task_id']
    # with open(os.path.join(btc.task_info_path, "task_%s.json" % task_id), "w") as f:
    #     json.dump(js1, f)
    with open(os.path.join(btc.task_log_path,"task_%s.out"% task_id), "w") as f:
        logging.logger.log(logging.Level.COMPULSORY, task_id,
                           "Init config for task_%s success!"% task_id,
                           heads=["CONFIG", "SUCCESS"])
    
    os.chdir(btc.task_space_path)
    if 'task_%s' % task_id not in os.listdir():
        os.mkdir('task_%s' % task_id)


