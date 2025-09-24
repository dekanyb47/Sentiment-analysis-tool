"""
Sentiment Analysis Tool

Analyzes and rates input text based on an evaluated score through a CLI.

Accepted forms of input:
- File input: -f/--file <file_path>
- Text input: -i/--input <text>

To run: python -m src.sentiment_analysis_tool [args]

Created by dekanyb47
2025
"""

import logging
from config.logging_config import setup_logging
logger = logging.getLogger(__name__)

import sys
import argparse

from src.engine import SentimentAnalyzer
from src.output_handling import output_results
from os.path import exists

def main():
    setup_logging()

    parser = argparse.ArgumentParser(prog="Sentiment Analysis Tool",
                                     description="Analyzes and rates reviews, comments etc. based on an evaluated score.",
                                     epilog="Example:")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Enter a file path for analysis")
    group.add_argument("-i", "--input", help="Enter some text for analysis")

    args = parser.parse_args()

    text = ""

    if args.file:
        if exists(args.file):
            with open(args.file, 'r', encoding="utf-8") as f:
                text = f.read()

        else:
            print(f"File '{args.file}' not found.")
            logger.error(f"File '{args.file}' not found.")


    else:
        text = args.input

    analysis = SentimentAnalyzer(text)
    output_results(analysis.analyzed_entries)
    logger.debug(f"Finished outputting results")


if __name__ == "__main__":
    setup_logging()

    main()