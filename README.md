readme not done yet







# Sentiment-analysis-tool
## A lightweight tool that analyzes input entries based on a bulit-in scoring system, and attempts to determine their sentiments. It does not use external stemming libraries, instead tries to determine the sentiment by finding keywords, negations and emphasizing words inside the input sentences.

All files and the entire logic of the program was written by me, while some of the testcases were written with AI.

---

## Installation

## Functions:
- built-in CLI (Command line interface)
- Analysis of words and their variations through a JSON-based database
- Handling form modifiers:
  `'nice' - positive (Score: 0.4)
'nice!' - positive (Score: 0.44)
'nice?' - neutral (Score: 0.08)
'nice!!' - positive (Score: 0.462)`

  `'not good at all' - very negative (Score: -0.603)
'not good AT ALL' - very negative (Score: -0.724)`
- Recognition of different word ordering (modular expressions):
   `'really not good' - negative (Score: -0.568)
  'not really good' - negative (Score: -0.237)`
- Scoring more complex entries with a decent accuracy:
  `'I bought this phone two weeks ago, and have been using it since. The camera is high-quality, and the battery life is alright as well. The only complaint I have is with the quality of the speakers. But considering the price point, I'm quite pleased with its performance.' - positive (Score: 0.434)
    I bought this phone two weeks ago, and have been using it since. - factual/unidentified (Score: 0.0)
    The camera is high-quality, and the battery life is alright as well. - positive (Score: 0.3)
    The only complaint I have is with the quality of the speakers. - factual/unidentified (Score: 0.0)
    But considering the price point, I'm quite pleased with its performance. - positive (Score: 0.56)`

Created by dekanyb47
2025
