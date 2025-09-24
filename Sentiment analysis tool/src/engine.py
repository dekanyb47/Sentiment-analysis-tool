"""
Groups together the logic of the whole program.
"""


import logging
logger = logging.getLogger(__name__)

from src.analyze import Analyze
from src.utils import ScoringContext, EntryAnalysis
from src.input_handling import break_text_into_entries
from src.json_imports import load_json_files_into_context

class SentimentAnalyzer():
    def __init__(self, text):
        self.text = text
        logger.info("Initialized SentimentAnalyzer object.")
        logger.debug(f"Given text: {self.text}")

        load_json_files_into_context()
        logger.info("Loaded all json files and updated context dataclass")

        self.entries = break_text_into_entries(self.text)
        logger.info(f"Broken text into entries")

        self.analyzed_entries = self.get_analysis_results()
        logger.info(f"Finished analysis.")

    
    def get_analysis_results(self) -> list[EntryAnalysis]:
        analyzer = Analyze(
            entries=self.entries,
            ctx=ScoringContext
        )

        return analyzer.entries
    

