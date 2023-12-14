import sys
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import ssl

'''
the input:
python wrapper.py -instance value_instance -param1 value1 -param2 value2......-cutoff_time value_cutoff_time
the output:
Result of this algorithm run:<STATUS>,<SCORE>,<ADDITIONAL RUNDATA>
'''

def run(model):
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = read_csv(url, names=names)

    array = dataset.values
    X = array[:, 0:4]
    Y = array[:, 4]
    validation_size = 0.3
    seed = 1
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)

    model.fit(X=X_train, y=Y_train)
    predictions = model.predict(X_validation)
    accuracy = accuracy_score(Y_validation, predictions)

    return accuracy


if __name__ == "__main__":
    C = None
    shrinking = None
    for i in range(len(sys.argv) - 1):
        if (sys.argv[i] == '-C'):
            C = float(sys.argv[i + 1])
        elif (sys.argv[i] == '-shrinking'):
            if sys.argv[i + 1] == "False":
                shrinking = False
            else:
                shrinking = True
    params = {}
    if C is not None:
        params["C"] = C
    if shrinking is not None:
        params["shrinking"] = shrinking

    model = SVC(**params)
    accuracy=run(model)
    print("Result of this algorithm run:<{}>,<{}>,<{}>".format('SUCCESS',accuracy,'None'))

