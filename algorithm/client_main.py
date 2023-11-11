import Logger.task_logging as logging
import os
import json
from Configs import bonline_task_config as btc

def init_task(js):
    js = json.loads(js)
    task_id=js['task_id']
    with open(os.path.join(btc.task_info_path, "task_%s.json" % task_id), "w") as f:
        json.dump(js, f)
    with open(os.path.join(btc.task_log_path,"task_%s.out"% task_id), "w") as f:
        logging.logger.log(logging.Level.COMPULSORY, task_id,
                           "Init config for task_%s success!"% task_id,
                           heads=["CONFIG", "SUCCESS"])
    os.chdir(btc.task_space_path)
    if 'task_%s' % task_id not in os.listdir():
        os.mkdir('task_%s' % task_id)


