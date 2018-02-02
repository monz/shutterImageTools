import __future__
import getopt
import os
import sys

import exifread


def readMetadata(path, extractKeys):
    f = open(path, 'rb')
    tags = exifread.process_file(f)
    data = {}

    for tag in tags.keys():
        if tag in (extractKeys):
            data.update({tag: tags[tag]})

    return data


def outputData(data, keys, delimiter):
    orderedList = []
    for key in keys:
        expression = str(data[key])
        if key == 'EXIF ISOSpeedRatings':
            value = str(evaluateValue(expression))
        else:
            value = '{:.3f}'.format(evaluateValue(expression))
        orderedList.append(value)
    print delimiter.join(orderedList)


def printHeader(data, delimiter):
    print delimiter.join(data)


def evaluateValue(expression):
    return eval(compile(expression, '<string>', 'eval', __future__.division.compiler_flag))


def readArgs():
    path = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["path="])
    except getopt.GetoptError:
        print sys.argv[0], '-p <path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print sys.argv[0], '-p <path> -n <sampleCount>'
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg

    return path


if __name__ == '__main__':
    # read command line options
    path = readArgs()

    extractKeys = ['EXIF ExposureTime', 'EXIF ISOSpeedRatings', 'EXIF ShutterSpeedValue', 'EXIF BrightnessValue']
    delimiter = ','
    printHeader(extractKeys, delimiter)
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            data = readMetadata(os.path.join(dirpath, filename), extractKeys)
            outputData(data, extractKeys, delimiter)