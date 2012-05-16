#!/usr/bin/env python
# emit top documents for a topic (in the order the documents appear in source file)
#  topic_weight_for_document  primary_id  secondary_id  topic_text
from sys import stdin
from sys import stdout
from optparse import OptionParser


usage = "usage: cat lda.docToTop.txt | %prog [options] topic_id documents"
parser = OptionParser(usage)
parser.add_option("-p", "--min_prob", dest="min_prob", default=0.0, help="minimum probability")
parser.add_option("-d", "--max_docs", dest="max_docs", default=10, help="maximum docs to output")

(options, args) = parser.parse_args()
if len(args) != 2:
    parser.error("incorrect number of arguments")
    parser.print_usage()
    exit(1)
    
import re
from heapq import *
import docToTop

# which topic are we getting?
target_topic = int(args[0])

# parse top docs
top_docs = []  # ( doc_id, prob of topic )
for line in stdin:
    primary_id, secondary_id, topic_probs = docToTop.parse(line)
    for topic, prob in topic_probs:
        if topic == target_topic and prob > float(options.min_prob):
            heappush(top_docs, (-float(prob), primary_id)) # -ve since we want top values in heap

if not top_docs:
    stdout.write('No docs found')
    exit(1)

# take top max_docs
primary_ids = set()
primary_id_to_prob = {}
for i in xrange(0, min(int(options.max_docs), len(top_docs))):
    (neg_prob, primary_id) = heappop(top_docs)
    primary_ids.add(primary_id)
    primary_id_to_prob[primary_id] = -neg_prob

# now grep document looking for these ids
for line in open(args[1]):
    primary_id = line.split(" ")[0]
    if primary_id in primary_ids:
        stdout.write("%s\t%s" % (primary_id_to_prob[primary_id], line))
        primary_ids.remove(primary_id)
        if len(primary_id)==0:
            exit(0)


