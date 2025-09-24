"""
analyze.py groups together the overall logic of the analysis.

A list of entries is passed in, and it analyzes each one entry's sentences seperately.
"""

import logging
logger = logging.getLogger(__name__)

from src.objects.group import group_keywords_with_modifiers, compute_group_score
from src.objects.negation import find_all_negations
from src.objects.keyword import find_all_positive_keywords, find_all_negative_keywords
from src.objects.emphasis import find_all_emphases
from src.form_modifiers import determine_punctuation_modifier, determine_casing_modifier

from config.constants import ROUNDING_DECIMALS

class Analyze:

    def __init__(self, entries, ctx):
        self.entries = entries          # a list of EntryAnalysis objects
        self.ctx = ctx

        for entry in self.entries:
            sentence_scores = {}

            for sentence in entry.sentences_in_entry:
                score = self.analyze_sentence(sentence)

                sentence_scores[sentence] = score
                logger.debug(f"Analyzed sentence {sentence} with a score of {score}.")

            entry.sentence_scores = sentence_scores

        for entry in self.entries:

            avg = self.calc_entry_avg_score(entry)
            entry.avg_score = avg


    def analyze_sentence(self, sentence) -> float:
        logger.debug(f"Starting analysis on sentence: {sentence}")

        # each of these arrays store objects of their respective classes
        positive_keywords = find_all_positive_keywords(sentence, self.ctx)
        negative_keywords = find_all_negative_keywords(sentence, self.ctx)
        keywords = positive_keywords + negative_keywords

        if not keywords:
            return 0.0

        negations = find_all_negations(sentence, self.ctx)
        negations.sort(key=lambda i:i.start_i)

        emphases = find_all_emphases(sentence, self.ctx)
        emphases.sort(key=lambda i:i.start_i)

        if negations:
            for i in negations:
                logger.debug(f"Negation found: '{i.phrase}' at position: {i.start_i}")
        if emphases:
            for i in emphases:
                logger.debug(f"Emphasis found: '{i.phrase}' at position: {i.start_i} with multiplier: {i.multiplier}")
        for i in keywords:
            logger.debug(f"Keyword found: '{i.word}' at position: {i.start_i} with base score: {i.base_score}")

        word_groups = group_keywords_with_modifiers(keywords, negations, emphases)

        for i in word_groups:
            logger.debug(f" Grouped keyword: {i.keyword.word}, with negation: {i.negation.phrase if i.negation else i.negation}, and emphases: {[e.phrase for e in i.emphases]}")

        group_scores = []

        for group in word_groups:
            score = compute_group_score(group, self.ctx)
            logger.debug(f"Computed group's base score as: {score}")
            
            casing_mod = determine_casing_modifier(sentence, group)
            score *= casing_mod

            group_scores.append(score)
        

        avg_score = sum(group_scores) / len(group_scores)

        punctuation_mod = determine_punctuation_modifier(sentence)

        avg_score = round(avg_score * punctuation_mod, 3)

        return avg_score

    # TODO: if needed, fine tune by calculating weighted avg based on the amount of keywords
    # TODO: if it ever will be possible to get a score of 0.0 on a sentence that has a keyword, (currently it's not) fix the skipping 

    # Calculates a weighted avg based on the length of sentences, skipping factual/unidentified sentences with a score of 0.0.
    def calc_entry_avg_score(self, entry):
        weighted_sum = 0
        total_length = 0

        for sentence, score in entry.sentence_scores.items():

            # skipping sentences with a score of 0.0
            if score == 0:
                continue

            weighted_sum += len(sentence) * score
            total_length += len(sentence)

        # if none of the sentences had a score that's not 0, we return
        if total_length == 0:
            return 0.0

        avg = weighted_sum / total_length
        return round(avg, ROUNDING_DECIMALS)
        


