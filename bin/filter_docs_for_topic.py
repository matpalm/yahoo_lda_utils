#!/usr/bin/env python

""" Filter out all members of a topic """

from sys import stdin
from sys import stdout
from sys import stderr
import docToTop
from optparse import OptionParser


usage = "usage: cat lda.docToTop.txt | %prog [options] topic_id documents"
parser = OptionParser(usage)
parser.add_option("-p", "--min_prob", dest="min_prob", default=0.0, help="docs over this minimum probability will be filtered out")

(options, args) = parser.parse_args()
if len(args) != 2:
    parser.error("incorrect number of arguments")
    parser.print_usage()
    exit(1)

# which topic are we getting?
target_topic = int(args[0])

# select the docs to be filtered out
primary_ids = set()
for line in stdin:
    primary_id, _, topic_probs = docToTop.parse(line)
    if any(topic == target_topic and prob >= float(options.min_prob) for topic, prob in topic_probs):
        primary_ids.add(primary_id)

if not primary_ids:
    stderr.write('No docs found')
    exit(1)

# now grep document looking for these ids
for line in open(args[1]):
    primary_id = line.split(" ")[0]
    if primary_id not in primary_ids:
        stdout.write(line)
        continue
    # perf
    primary_ids.remove(primary_id)
    if not primary_ids:
        exit(0)
