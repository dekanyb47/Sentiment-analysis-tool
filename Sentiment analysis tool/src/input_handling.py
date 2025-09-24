import logging
logger = logging.getLogger(__name__)

from src.utils import EntryAnalysis
from config.constants import ENTRY_SPLITTING_STR

def break_text_into_entries(text) -> list[EntryAnalysis]:
    entry_txts = [e for e in text.split(ENTRY_SPLITTING_STR) if e]
    logger.debug(f"Entries: {entry_txts}")

    entry_objects = []

    for entry_txt in entry_txts:
        entry_obj = EntryAnalysis()

        sentences = break_into_sentences(entry_txt)
        logger.debug(f"Broke up entry into sentences: {sentences}")

        entry_obj.entry = entry_txt
        entry_obj.sentences_in_entry = sentences

        entry_objects.append(entry_obj)

    return entry_objects


def break_into_sentences(text) -> list[str]:
    sentence_end_punctuation = ['.', '!', '?']
    sentences = []

    l = 0
    for r, char in enumerate(text):
        if char in sentence_end_punctuation:
            if l == r:      # if we enounter a sentence ending punc. after another one, we simply add it to the previous string.
                if sentences:
                    sentences[-1] += char

            else:
                sentences.append(text[l:r + 1].strip())

            l = r + 1

    
    # if there's any text left we didn't add because it didn't end with a punctuation, we add it regardless.
    leftover = text[l:].strip()
    if leftover:
        sentences.append(leftover)

    return sentences
