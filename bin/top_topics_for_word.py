#!/usr/bin/env python
# emit top topics for a word
# usage: top_topics_for_word.py japan lda.topToWor.txt

import sys
if len(sys.argv) != 3:
    print >>sys.stderr, "usage: %s word lda.topToWor.txt" % (sys.argv[0])
    exit(1)

import re
from heapq import *
import topToWor

# which word are we getting?
target_word = sys.argv[1]

# parse top topics
top_topics = []  # ( topic_id, prob of word )
for line in open(sys.argv[2]):
    topic_id, word_prob_pairs = topToWor.parse(line)
    for word, prob in word_prob_pairs:
        if word == target_word:
            heappush(top_topics, (-prob, topic_id)) # -ve since we want >

# take top 10
num_emitted = 0
while len(top_topics) > 0 and num_emitted < 10:
    (neg_prob, topic_id) = heappop(top_topics)
    print -neg_prob, topic_id
    num_emitted += 1
