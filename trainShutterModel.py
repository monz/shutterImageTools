import re
import sys
import getopt
import os
from scipy.misc.pilutil import imread
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn import svm


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
        print sys.argv[0], '-p <path>'
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

    regex = re.compile("(closed|open)")
    flat, targ = trainInfo(path, regex)

    X_train, X_test, y_train, y_test = train_test_split(flat, targ, test_size = 0.3, random_state = 0)

    clf = svm.SVC(kernel='linear', C=1)
    clf.fit(X_train, y_train)

    joblib.dump(clf, 'shutterModel.pkl')

    print clf.score(X_test, y_test)

    print clf.coef_
    print clf.intercept_