import sys

'''
the input:
python wrapper.py -instance value_instance -param1 value1 -param2 value2......-cutoff_time value_cutoff_time
the output:
Result of this algorithm run:<STATUS>,<SCORE>,<ADDITIONAL RUNDATA>
'''

status='FAILED'
def run(params) -> float:
    x=params['x']
    return x ** 2

if __name__=='__main__':
    x = None
    for i in range(len(sys.argv) - 1):
        if (sys.argv[i] == '-x'):
            x = float(sys.argv[i + 1])
    params = {}
    if x is not None:
        params['x'] = x
    score=run(params)
    if score is not None:
        STATUS='SUCCESS'
    print("Result of this algorithm run:<{}>,<{}>,<{}>".format(status,score,'None'))