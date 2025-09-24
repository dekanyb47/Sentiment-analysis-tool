"""
The class WordGroup groups keywords together with their associated negations and emphases. Contains the class' definition and all
related functions.
Only one keyword and negation per group.
"""

import logging
logger = logging.getLogger(__name__)

from src.objects.negation import apply_negation_modifier
from src.objects.emphasis import apply_emphases_modifier
from config.constants import MODULATED_NEGATION_SOFTENING_FACTOR

# TODO: rewrite to a dataclass when I feel like it
class WordGroup:
    def __init__(self, keyword, negation=None, emphases=None, score=0.0):
        self.keyword = keyword
        self.negation = negation
        self.emphases = emphases if emphases else []
        self.score = score


def group_keywords_with_modifiers(keywords, negations, emphases):

    # group up emphases and negations with the keyword they belong to
    word_groups = []
    neg_i = 0
    emp_i = 0

    for i, keyword in enumerate(keywords):

        # TODO: maybe set a limit of 50 chars for distances to count, if that returns more accurate results.
        group = WordGroup(keyword=keywords[i])

        # gets the nearest negation to the keyword and adds it to the group.
        while neg_i < len(negations) and negations[neg_i].start_i < keyword.start_i: 
            group.negation = negations[neg_i]
            neg_i += 1

        while emp_i < len(emphases):
            emphasis = emphases[emp_i]
            distance_to_curr = abs(emphasis.start_i - keyword.start_i)

            if i + 1 < len(keywords):
                next_keyword = keywords[i + 1]
                distance_to_next = abs(next_keyword.start_i - emphasis.start_i)
            else:
                distance_to_next = float('inf')

            if distance_to_curr <= distance_to_next:
                group.emphases.append(emphasis)
                emp_i += 1
            else:
                break

        word_groups.append(group)
            

    return word_groups

# If it is a modulated negation, it returns the modulating emphasis. (e.g. "not *really* good"), otherwise None.
def is_modulated_negation(group):
    for i, emp in enumerate(group.emphases):
        if group.negation.start_i < emp.start_i < group.keyword.start_i:
            return emp


def compute_group_score(group, ctx):
    base_val = group.keyword.base_score

    if not group.negation and not group.emphases:
        return base_val

    elif group.negation and not group.emphases:
        return apply_negation_modifier(base_val)

    elif not group.negation and group.emphases:
        return apply_emphases_modifier(base_val, group.emphases)

    else:
        # 2 cases: if there's an emphasizing word between the keyword and the negating word: "the quality is (really) not that good." - (modulated negation)
        #          if there's no emphasizing word between the two: '(seriouly) not a bad product."

        score_with_negation = apply_negation_modifier(base_val)
        modulating_emp = is_modulated_negation(group)

        if not modulating_emp:
            return apply_emphases_modifier(score_with_negation, group.emphases)

        else:
            group.emphases.remove(modulating_emp)   # we don't want to use the modulating emphasis

            # TODO: if the .json files are updated, and it would make sense to differnciate emphases with a multiplier above and below 1, implement that
            softened_score = score_with_negation * MODULATED_NEGATION_SOFTENING_FACTOR
            return apply_emphases_modifier(softened_score, group.emphases)
            

