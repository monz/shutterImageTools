#!/bin/bash
python2 findShutterImages.py -p resized | awk '{split($0,a,":"); print "mkdir -p",a[1],"&&","cp",a[2],a[1]}' | bash
