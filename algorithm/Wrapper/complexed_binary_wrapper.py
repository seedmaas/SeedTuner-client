import sys, os, time, re
import subprocess

'''
the basic input:
python3 wrapper.py -instance value_instance -param1 value1 -param2 value2......-cutoff_time value_cutoff_time
the output:
Result of this algorithm run:<STATUS>,<SCORE>,<ADDITIONAL RUNDATA>
'''

status='FAILED'
cutoff_time=None
buffer=20

def getParamsDict(argv):
    instance = None
    for i in range(len(argv) - 1):
        if (sys.argv[i] == '-cutoff_time'):
            cutoff_time = float(argv[i + 1])
        elif (sys.argv[i] == '-instance'):
            instance = argv[i + 1]
    paramsDict = {}
    if instance is not None:
        paramsDict["inst"] = instance
    return paramsDict


def combineCMD(paramsDict):
    cmd = "./PbO-CCSAT"
    for name, value in paramsDict.items():
        cmd += " -%s %s" % (name, value)
    return cmd


def parse(output):
    if (re.search('s SATISFIABLE', output) or re.search('s UNSAT', output)):
        return 1.0
    return 0.0


def run(cmd):
    score = None
    try:
        proc = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  timeout=(cutoff_time+buffer))
        score = parse(proc.stdout.decode())
        if score is not None:
            status='SUCCESS'
    except subprocess.TimeoutExpired:
        score = None
        status='TIMEOUT'
    return score


if __name__ == '__main__':
    paramsDict = getParamsDict(sys.argv)
    cmd = combineCMD(paramsDict)
    score = run(cmd)
    print("Result of this algorithm run:<{}>,<{}>,<{}>".format(status,score,'None'))



