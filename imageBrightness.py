import numpy
import cv2
import time


def current_millis():
    return int(round(time.time() * 1000))


def duration(start, end, msg='', prompt='Duration'):
    print '{}: {}, {} ms.\n'.format(prompt, msg, end - start)


closedImg = '/var/vms/pics/2017-10-26_auto/pic_1509000612.jpg'  # closed
openImg = '/var/vms/pics/2017-10-26_auto/pic_1509012052.jpg'  # open

start = current_millis()
imgC = cv2.imread(closedImg)
duration(start, current_millis(), 'read closed img')

start = current_millis()
imgO = cv2.imread(openImg)
duration(start, current_millis(), 'read open img')

start = current_millis()
[b, g, r] = cv2.split(imgC)
duration(start, current_millis(), 'split')

start = current_millis()
print 'red {} sd {}'.format(numpy.average(r), numpy.std(r))
print 'green {} sd {}'.format(numpy.average(g), numpy.std(g))
print 'blue {} sd {}'.format(numpy.average(b), numpy.std(b))
duration(start, current_millis(), 'average')

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
print numpy.average(rRand)
print numpy.average(gRand)
print numpy.average(bRand)
duration(start, current_millis(), 'averageSampled')

start = current_millis()
print "std:"
print numpy.std(rRand) / numpy.sqrt(sc)
print numpy.std(gRand) / numpy.sqrt(sc)
print numpy.std(bRand) / numpy.sqrt(sc)
duration(start, current_millis(), 'stdSampled')
