#!/usr/bin/env
import re

def parse(line):
    topic_id, tokens = re.match("^Topic (\d*): (.*)", line.strip()).groups()
    word_prob_pairs = re.sub("[\(\)]","",tokens).split(" ")
    word_probs = []
    for pair in word_prob_pairs:
        word, prob = pair.split(",")
        word_probs.append((word, float(prob)))
    return ( topic_id, word_probs )

    
    
