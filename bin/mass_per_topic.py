#!/usr/bin/env python
# output total probability mass per topic
# usage: mass_per_topic.py < lda.docToTop.txt 

import sys
from collections import defaultdict
import docToTop
from optparse import OptionParser

usage = "usage: cat %prog [options] < lda.docToTop.txt"
parser = OptionParser(usage)
parser.add_option("-p", "--min_prob", dest="min_prob", default=0.0, help="minimum probability")
(options, _) = parser.parse_args()

total_mass = defaultdict(float)

for line in sys.stdin: 
    id1, id2, topic_probs = docToTop.parse(line)
    for topic, prob in topic_probs:
        if float(prob) >= float(options.min_prob):
            total_mass[topic] += prob

for k, v in total_mass.iteritems():
    print "%s\t%s" % (k,v)
