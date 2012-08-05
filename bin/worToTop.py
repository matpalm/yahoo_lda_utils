#!/usr/bin/env
import re
from collections import defaultdict
from numpy.linalg import *

WORD_TOPIC_PAIR_RE = re.compile("(.*),(\d*)")

def parse(line, normalise=True, chop=1.0):
    primary_id, secondary_id, topics = line.strip().split("\t")
    word_topic_pairs = re.sub("[\(\)]","",topics).split(" ")
    # collect topics
    topics = defaultdict(int)
    for pair in word_topic_pairs:
        word, topic = re.match(WORD_TOPIC_PAIR_RE, pair).groups()
        topics[topic] += 1

    if not normalise:
        return ( primary_id, secondary_id, topics )

    # normalise and chop
    magnitude = norm(topics.values())
    chop_sqr = chop * chop
    cumsum_sqr = 0.0
    chopped_topics = {}
    for topic, freq in sorted(topics.iteritems(), key=lambda tf: -tf[1]):        
        n_freq = float(freq) / magnitude
        chopped_topics[topic] = n_freq
        cumsum_sqr += n_freq * n_freq
        if cumsum_sqr > chop_sqr:
            break
    return ( primary_id, secondary_id, chopped_topics )

    
    
