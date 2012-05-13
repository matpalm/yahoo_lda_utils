#!/usr/bin/env python
# output total probability mass per topic
# usage: cat mass_per_topic.py < lda.docToTop.txt 

import sys
from collections import defaultdict
import docToTop

total_mass = defaultdict(float)

for line in sys.stdin: 
    id1, id2, topic_probs = docToTop.parse(line)
    for topic, prob in topic_probs:
        total_mass[topic] += prob

for k, v in total_mass.iteritems():
    print "%s\t%s" % (k,v)
