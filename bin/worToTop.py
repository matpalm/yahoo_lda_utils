#!/usr/bin/env
import re
from collections import defaultdict
from numpy.linalg import *

def parse(line):
    primary_id, secondary_id, topics = line.strip().split("\t")
    word_topic_pairs = re.sub("[\(\)]","",topics).split(" ")
    # collect topics
    topics = defaultdict(int)
    for pair in word_topic_pairs:
        word, topic = pair.split(",")
        topics[topic] += 1
    # normalise (with cumsum chop at 0.99)
    magnitude = norm(topics.values())
    chop = 0.99 * 0.99
    cumsum = 0.0
    chopped_topics = {}
    for topic, freq in sorted(topics.iteritems(), key=lambda tf: -tf[1]):        
        n_freq = float(freq) / magnitude
        chopped_topics[topic] = n_freq
        cumsum += n_freq * n_freq
        if cumsum > chop:
            break
    # done
    return ( primary_id, secondary_id, chopped_topics )

    
    
