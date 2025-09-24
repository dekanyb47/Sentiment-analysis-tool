from dataclasses import dataclass, field

@dataclass
class ScoringContext:
    positive_words : dict
    negative_words : dict
    negating_phrases : dict
    emphasizing_phrases : dict


@dataclass
class EntryAnalysis:
    entry : str = ""
    sentences_in_entry : list[str] = field(default_factory=list)
    sentence_scores : dict[str, float] = field(default_factory=dict)
    avg_score : float = 0.0
