"""
Emphases strengthen or weaken the sentiment of a keyword. Contains the class definition and all related functions.
Examples: "very", "somewhat" etc.
"""


import logging
logger = logging.getLogger(__name__)

from re import finditer, escape, IGNORECASE

from config.constants import EMPHASIS_SCALING_BASE


class Emphasis:
    def __init__(self, phrase, multiplier, start_i):
        self.phrase = phrase
        self.multiplier = multiplier
        self.start_i = start_i


def find_all_emphases(sentence, ctx):
    emphases = []

    # TODO: this is pretty inefficient, might need a rework if there will be more words added.
    for phrase, multiplier in ctx.emphasizing_phrases.items():
        for match in finditer(r'\b' + escape(phrase) + r'\b', sentence, IGNORECASE):

            found_phrase = sentence[match.start():match.end()]        # retains casing
            emphases.append(Emphasis(found_phrase, multiplier, match.start()))

    return emphases


def apply_emphases_modifier(score, emphases):
    for exponent_power, emp in enumerate(emphases):

        # a limit of 10 is added, so the exponent's value can never accidentally reach 0.
        if exponent_power == 10:
            break

        base_multiplier = emp.multiplier

        score += score * (base_multiplier - 1) * (EMPHASIS_SCALING_BASE ** exponent_power)
    
    return score