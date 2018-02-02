import getopt
import os
import sys
import time

import cv2
import numpy
from scipy import stats


def current_millis():
    return int(round(time.time() * 1000))


def duration(start, end, msg='', prompt='Duration'):
    print '{}: {}, {} ms.\n'.format(prompt, msg, end - start)


def ci(x, confidence=0.95):
    n = len(x)
    m, se = numpy.mean(x), stats.sem(x)
    z = stats.t.ppf((1 + confidence) / 2., n - 1)
    h = z*se
    return m, m-h, m+h


def split(img):
    r = img[:, :, 2]
    g = img[:, :, 1]
    b = img[:, :, 0]
    return [r,g,b]

def flatten(r,g,b):
    rf = r.flatten()
    gf = g.flatten()
    bf = b.flatten()
    return [rf, gf, bf]


def brightness(img, n):
    [r,g,b] = split(img)
    [red,green,blue] = flatten(r,g,b)

    rRed = numpy.random.choice(red, n)
    rGreen = numpy.random.choice(green, n)
    rBlue = numpy.random.choice(blue, n)

    bRed = numpy.average(rRed)
    bGreen = numpy.average(rGreen)
    bBlue = numpy.average(rBlue)

    return [bRed, bGreen, bBlue]

def readArgs():
    path = ''
    sampleCount = 10000
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:n:", ["path=", "sampleCount="])
    except getopt.GetoptError:
        print sys.argv[0], '-p <path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0], '-p <path> -n <sampleCount>'
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-n", "--sampleCount"):
            sampleCount = arg

    return path, sampleCount


if __name__ == '__main__':
    # read command line options
    path, sampleCount = readArgs()

    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            img = cv2.imread(os.path.join(dirpath, filename))
            [r,g,b] = brightness(img, sampleCount)
            print '{:s}:{:.3f}:{:.3f}:{:.3f}'.format(filename, r, g, b)

