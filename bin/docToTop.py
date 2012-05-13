#!/usr/bin/env
import re

def parse(line):
    primary_id, secondary_id, topics = line.strip().split("\t")
    topic_prob_pairs = re.sub("[\(\)]","",topics).split(" ")
    topic_probs = []
    for pair in topic_prob_pairs:
        topic, prob = pair.split(",")
        topic_probs.append((int(topic), float(prob)))
    return ( primary_id, secondary_id, topic_probs )

    
    
