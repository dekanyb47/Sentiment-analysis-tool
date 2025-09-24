from config.logging_config import setup_logging
import logging
setup_logging()

from src.sentiment import determine_sentiment

def output_results(rated_entries):
    for entry in rated_entries:
        entry_sentiment = determine_sentiment(entry.avg_score)

        print(f"\n'{entry.entry}' - {entry_sentiment} (Score: {entry.avg_score})")

        for sentence, sentence_score in entry.sentence_scores.items():
            sentence_sentiment = determine_sentiment(sentence_score)

            print(f"    {sentence} - {sentence_sentiment} (Score: {sentence_score})")