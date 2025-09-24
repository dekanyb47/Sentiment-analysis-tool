"""
Keywords can be either positive or negative. This file contains the Keyword class' definition, and all related functions.
Examples: "good", "bad", "terrible" etc.
"""

from re import finditer, escape, IGNORECASE

import logging
logger = logging.getLogger(__name__)

class Keyword:
    def __init__(self, word, base_score, start_i):
        self.word = word
        self.start_i = start_i
        self.base_score = base_score

        if self.base_score >= 0:
            self.score_is_positive = True
        else:
            self.score_is_positive = False


# TODO: rework for efficiency if needed.
def find_all_negative_keywords(sentence, ctx) -> list:
    negative_keywords = []

    for word, score in ctx.negative_words.items():
        for match in finditer(r'\b' + escape(word) + r'\b', sentence, IGNORECASE):

            found_word = sentence[match.start():match.end()]        # retains casing
            negative_keywords.append(Keyword(found_word, score, match.start()))

    return negative_keywords


def find_all_positive_keywords(sentence, ctx) -> list:
    positive_keywords = []

    for word, score in ctx.positive_words.items():
        for match in finditer(r'\b' + escape(word) + r'\b', sentence, IGNORECASE):

            found_word = sentence[match.start():match.end()]        # retains casing
            positive_keywords.append(Keyword(found_word, score, match.start()))

    return positive_keywords