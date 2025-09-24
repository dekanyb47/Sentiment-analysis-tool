import logging
logger = logging.getLogger(__name__)

from config.constants import (
    VERY_POSITIVE_BOUNDARY,
    VERY_NEGATIVE_BOUNDARY,
    POSITIVE_BOUNDARY,
    NEGATIVE_BOUNDARY
)

def determine_sentiment(score):
    if score == 0.0:
        return "factual/unidentified"
    if score <= VERY_NEGATIVE_BOUNDARY:
        return "very negative"
    elif score <= NEGATIVE_BOUNDARY:
        return "negative"
    elif score < POSITIVE_BOUNDARY:
        return "neutral"
    elif score < VERY_POSITIVE_BOUNDARY:
        return "positive"
    else:
        return "very positive"