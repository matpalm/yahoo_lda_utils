#!/usr/bin/env python                                                                                                                                               
# emit topic frequencies per document (l2 normalised)
# (like a more complete version of lda.docToTop.txt

import sys
import worToTop
from optparse import OptionParser

usage = "usage: cat lda.worToTop.txt | %prog [options]"
parser = OptionParser(usage)
parser.add_option("-n", "--normalise", dest="normalise", default=False, help="whether to l2 normalise")
parser.add_option("-c", "--chop", dest="chop", default=1.0, help="cumsum chop (if normalising)")

(options, args) = parser.parse_args()
if len(args) != 0:
    parser.error("incorrect number of arguments")
    parser.print_usage()
    exit(1)

for line in sys.stdin:
    id1, id2, topic_counts = worToTop.parse(line, bool(options.normalise), float(options.chop))
    for topic, freq in topic_counts.iteritems():
        print "\t".join(map(str, [id1, id2, topic, "%.15f" % freq]))
