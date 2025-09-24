"""
Negations are words or phrases that reverse the sentiment of a keyword. This file contains the Negation class' definition, 
and all related functions.
Examples: "not", "would be" etc.
"""

from re import finditer, escape, IGNORECASE

import logging
logger = logging.getLogger(__name__)

class Negation:
    def __init__(self, phrase, start_i):
        self.phrase = phrase
        self.start_i = start_i

        
def find_all_negations(sentence, ctx):
    negations = []

    for phrase in ctx.negating_phrases.keys():
        for match in finditer(r'\b' + escape(phrase) + r'\b', sentence, IGNORECASE):
            found_phrase = sentence[match.start():match.end()]
            negations.append(Negation(found_phrase, match.start()))

    return negations

# TODO: remove the magic numbers
def apply_negation_modifier(base_val):

    # positive: 
    if base_val > 0:
        return -0.43 + base_val / 4

    # negative:
    else:
        return 0.3 + base_val / 1.7