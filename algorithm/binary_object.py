import copy
import multiprocessing
import threading

from threading import Thread,Lock
from concurrent.futures import ThreadPoolExecutor
from Configs import bonline_task_config as btc


#method to get the performance of the solver
def binary_object(solver,total_performance, detail_list,task_id, target,coreNum=3):
    solver = copy.deepcopy(solver)
    if btc.instance_length==0:
        solver.solve(task_id,total_performance,detail_list)
    else:
        performanceList=doMutiSolve(solver=solver,task_id=task_id,coreNum=btc.instance_length,detail_list=detail_list)
        total_performance.append(sum(performanceList)/len(performanceList))

# method to use the solver return performancelist on multi_instances
def doMutiSolve(task_id,solver,coreNum,detail_list)->list:
    executor = ThreadPoolExecutor(max_workers=coreNum)
    performanceList = []
    all_task=[]
    # for _ in range(btc.instance_length):
    instance_solver = copy.deepcopy(solver)
    all_task.append(executor.submit(instance_solver.solve,task_id,performanceList,detail_list))
    result = [i.result() for i in all_task]
    executor.shutdown()
    return performanceList
