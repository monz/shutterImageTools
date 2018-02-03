import getopt
import os
import re
import sys

import numpy as np
from scipy.misc.pilutil import imread
from sklearn import svm
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split


def flatten(filename):
    img = imread(filename)
    return img.flatten()


def target(filename, regex):
    m = regex.match(filename)
    if m is not None:
        return m.group()
    else:
        return "NA"


def trainInfo(path, regex):
    flat = []
    targ = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            flat.append(flatten(os.path.join(dirpath, filename)))
            targ.append(target(filename, regex))
    return flat, targ


def readArgs():
    path = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["path="])
    except getopt.GetoptError:
        print sys.argv[0], '-h (for help)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0], '-p <path>'
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg

    return path


if __name__ == '__main__':
    # read command line options
    path = readArgs()

    random_state = np.random.RandomState(0)
    regex = re.compile("(closed|open)")
    flat, targ = trainInfo(path, regex)

    X_train, X_test, y_train, y_test = train_test_split(flat, targ, test_size = 0.3, random_state = random_state)

    clf = svm.SVC(kernel='linear', C=1)
    clf.fit(X_train, y_train)

    joblib.dump(clf, 'shutterModel.pkl')

    # evaluate model
    y_score = clf.predict(X_test)

    truePositives = 0
    falsePositives = 0
    falseNegatives = 0
    n = len(y_test)
    for i in range(0, n):
        if (y_test[i] == 'closed') and (y_score[i] == 'closed'):
            truePositives += 1
        elif (y_test[i] == 'closed') and (y_score[i] == 'open'):
            falsePositives += 1
        elif (y_test[i] == 'open') and (y_score[i] == 'closed'):
            falseNegatives += 1

    precision = float(truePositives) / (truePositives + falsePositives)
    recall = float(truePositives) / (truePositives + falseNegatives)
    fscore = float(2*(precision*recall)) / (precision + recall)

    print("TruePositives: ", truePositives)
    print("FalsePositives: ", falsePositives)
    print("falseNegatives: ", falseNegatives)

    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-Score: ", fscore)