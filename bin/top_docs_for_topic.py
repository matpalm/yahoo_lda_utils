#!/usr/bin/env python
# emit top documents for a topic (in the order the documents appear in source file)
#  topic_weight_for_document  primary_id  secondary_id  topic_text
 
import sys
if len(sys.argv) != 3:
    print >>sys.stderr, "usage: cat lda.docToTop.txt | %s topic_id documents" % (sys.argv[0])
    exit(1)
    
import re
from heapq import *
import docToTop

# which topic are we getting?
target_topic = int(sys.argv[1])

# parse top docs
top_docs = []  # ( doc_id, prob of topic )
for line in sys.stdin:
    primary_id, secondary_id, topic_probs = docToTop.parse(line)
    for topic, prob in topic_probs:
        if topic == target_topic:
            heappush(top_docs, (-float(prob), primary_id)) # -ve since we want top values in heap

# take top 10
primary_ids = set()
primary_id_to_prob = {}
for i in xrange(0, 10):
    (neg_prob, primary_id) = heappop(top_docs)
    primary_ids.add(primary_id)
    primary_id_to_prob[primary_id] = -neg_prob

# now grep document looking for these 10 ids
for line in open(sys.argv[2]):
    primary_id = line.split(" ")[0]
    if primary_id in primary_ids:
        sys.stdout.write("%s\t%s" % (primary_id_to_prob[primary_id], line))
        primary_ids.remove(primary_id)
        if len(primary_id)==0:
            exit(0)


