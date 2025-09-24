"""
Form modifiers are extra modifiers that are calculated in after the base score of a sentence has been analyzed. These include:
- UPPERCASE words
- sentence ending punctuation (!, ?, ...)
"""

import logging
logger = logging.getLogger(__name__)

from config.constants import (
    QUESTION_SCORE_SOFTENING_MULTIPLIER,
    PUNCTUATION_SCALING_BASE,
    EXCLAMATION_MARK_BASE_MULTIPLIER,
    UPPERCASE_MULTIPLIER,
    ELIPSIS_MULTIPLIER
)

# one sentence can contain no more than one contiguous substring consisting of only sentence ending punctuation (. ! ? \n). 
# this substring is always at the end of the sentence.
def count_sentence_ending_punctuation(sentence) -> dict:
    punctuation_count = {'!': 0,
                         '?': 0,
                         '.': 0}

    for i in range(len(sentence) - 1, -1, -1):
        if sentence[i] not in punctuation_count:
            break
        else:
            punctuation_count[sentence[i]] += 1

    return punctuation_count


def determine_punctuation_modifier(sentence):
    punctuation_count = count_sentence_ending_punctuation(sentence)
    logger.debug(f"Punctuations counted in sentence: {punctuation_count}")

    modifier = 1
    exclamation_mark_c = punctuation_count['!']
    question_mark_c = punctuation_count['?']
    period_c = punctuation_count['.']

    if exclamation_mark_c == 0 and question_mark_c == 0:
        if period_c < 3:
            return 1

        # we don't differentiate cases where there's elipsis (three periods) AND other punctuations from the ones where there's ONLY punctuation.
        else:
            return ELIPSIS_MULTIPLIER

    elif exclamation_mark_c == 0 and question_mark_c > 0:
        # TODO: make more accurate guesses as to what kind of question it may be. 
            # (e.g. 'how can this be so bad?' or 'why are people saying it's bad?')
        return QUESTION_SCORE_SOFTENING_MULTIPLIER

    else:
        # in the case where both ! and ? are used, they are most likely both for strengthening the sentence (e.g. how can the quality be this bad??!!)
        # so, we can compute the result as if there were only exclamation marks.

        total_count = exclamation_mark_c + question_mark_c

        # a limit of 10 is added, so the exponent's value never accidentally reaches 0.
        for exponent_power in range(min(total_count, 10)):
            modifier += modifier * (EXCLAMATION_MARK_BASE_MULTIPLIER - 1) * (PUNCTUATION_SCALING_BASE ** exponent_power)
        
        return modifier


def determine_casing_modifier(sentence, group):
    if any(emp.phrase.isupper() for emp in group.emphases) or (
        group.negation and group.negation.phrase.isupper()) or (
        group.keyword.word.isupper()):

        return UPPERCASE_MULTIPLIER

    else:
        return 1

