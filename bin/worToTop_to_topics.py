#!/usr/bin/env python                                                                                                                                               
# emit topic frequencies per document (l2 normalised)
# (like a more complete version of lda.docToTop.txt
# usage: worToTop_to_topics.py < lda.worToTop.txt

import sys
import worToTop

for line in sys.stdin:
    id1, id2, topic_counts = worToTop.parse(line)
    for topic, freq in topic_counts.iteritems():
        print "\t".join(map(str, [id1, id2, topic, "%.15f" % freq]))
