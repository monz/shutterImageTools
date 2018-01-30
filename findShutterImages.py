import getopt
import os
import sys

from scipy.misc.pilutil import imread
from sklearn.externals import joblib


def flatten(filename):
    img = imread(filename)
    return img.flatten()


def readArgs():
    path = ''
    model = 'shutterModel.pkl'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpm:", ["path=", "model="])
    except getopt.GetoptError:
        print sys.argv[0], '-p <path> -m <model>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0], '-p <path> -m <model>'
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-m", "--model"):
            model = arg

    return path, model


if __name__ == '__main__':
    # read command line options
    path, model = readArgs()

    clf = joblib.load(model)

    for (dirpath, dirnames, filenames) in os.walk(path):
        # ignore sub folders
        for filename in filenames:
            file = os.path.join(dirpath, filename)
            print "%s:%s" % (clf.predict(flatten(file).reshape(1, -1))[0], file)
