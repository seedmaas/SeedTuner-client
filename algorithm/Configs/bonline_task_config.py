import os
import json


python_version = "python3.9"

MAX_EXECUTE_TIME = 172800
# about log
task_log_handler = 2  # TERMINAL = 0 FILE = 1 TERMINAL_AND_FILE = 2
task_log_level = 0  # DEBUG = 0 INFO = 1 WARNING = 2 COMPULSORY = 3

instance_length=5
current_path = os.getcwd()+'/algorithm'
task_root_path=os.path.join(current_path, "BOnlineTask")
task_storage_path = os.path.join(task_root_path, "task_storage")
task_info_path = os.path.join(task_storage_path, "task_info")
task_space_path = os.path.join(task_storage_path, "task_space")
task_log_path = os.path.join(task_storage_path, "task_log")

pids_path=task_space_path


def get_task_pids_path(task_id):
    return os.path.join(task_space_path,'task_'+task_id,'pids.txt')

def get_info(task_id,name):
    with open(os.path.join(task_info_path,"task_%s.json"% task_id), "r") as json_file:
     data = json.load(json_file)
     if name=='muti_instances':
         return os.listdir(data['muti_instances'])
     else:
         return data[name]
     
     
