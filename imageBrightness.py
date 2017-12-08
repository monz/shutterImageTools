import numpy
import cv2
import time
from scipy import stats


def current_millis():
    return int(round(time.time() * 1000))


def duration(start, end, msg='', prompt='Duration'):
    print '{}: {}, {} ms.\n'.format(prompt, msg, end - start)


def ci(x, confidence=0.95):
    n = len(x)
    m, se = numpy.mean(x), stats.sem(x)
    z = stats.t.ppf((1 + confidence) / 2., n - 1)
    #z = 1.96
    h = z*se
    return m, m-h, m+h


closedImg = '/var/vms/pics/2017-10-26_auto/pic_1509000612.jpg'  # closed
openImg = '/var/vms/pics/2017-10-26_auto/pic_1509012052.jpg'  # open

start = current_millis()
imgC = cv2.imread(closedImg)
duration(start, current_millis(), 'read closed img')

start = current_millis()
imgO = cv2.imread(openImg)
duration(start, current_millis(), 'read open img')

img = imgC

start = current_millis()
[b, g, r] = cv2.split(img)
duration(start, current_millis(), 'split')

start = current_millis()
b = img[:, :, 0]
g = img[:, :, 1]
r = img[:, :, 2]
duration(start, current_millis(), 'split numpy')

start = current_millis()
print 'red {} sd {}'.format(numpy.average(r), numpy.std(r))
print 'green {} sd {}'.format(numpy.average(g), numpy.std(g))
print 'blue {} sd {}'.format(numpy.average(b), numpy.std(b))
duration(start, current_millis(), 'average + std')

start = current_millis()
rf = r.flatten()
gf = g.flatten()
bf = b.flatten()
duration(start, current_millis(), 'flatten')

start = current_millis()
sc = 10000
rRand = numpy.random.choice(rf, sc)
gRand = numpy.random.choice(gf, sc)
bRand = numpy.random.choice(bf, sc)
duration(start, current_millis(), 'sample')

start = current_millis()
rRand = numpy.sort(rRand)
gRand = numpy.sort(gRand)
bRand = numpy.sort(bRand)
duration(start, current_millis(), 'sort')

start = current_millis()
print "avg:"
ru = numpy.average(rRand)
gu = numpy.average(gRand)
bu = numpy.average(bRand)

rsem = stats.sem(rRand, ddof=1)
gsem = stats.sem(gRand, ddof=1)
bsem = stats.sem(bRand, ddof=1)

print 'red {} sd {}'.format(ru, rsem)
print 'green {} sd {}'.format(gu, gsem)
print 'blue {} sd {}'.format(bu, bsem)

duration(start, current_millis(), 'averageSampled + sem')

start = current_millis()
print ci(rRand)
print ci(gRand)
print ci(bRand)
duration(start, current_millis(), 'ci')
