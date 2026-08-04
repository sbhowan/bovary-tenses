# _Madame Bovary_ Verb Tense Analysis
This program counts the distribution of finite verb tenses in the French text of Gustave Flaubert's _Madame Bovary_, comparing usage across two registers:
* Dialogue
* Narration

It uses spaCy’s French morphological tagger (```fr_core_news_md```) to identify finite verbs and auxiliaries, assign tense labels, and produce a summary table.

## Research Question
In 19th-century French fiction, narration often relies on the passé simple and imparfait tenses for storytelling and exposition, while dialogue is more temporal and tends to skew toward présent, futur, conditionnel, and impératif. By looking at different verb tenses throughout the novel and comparing their distributions, we can investigate how tense encodes discourse structure.

## Requirements
Install spaCy with ```pip install spacy``` and the medium French model with ```python -m spacy download fr_core_news_md```.

## Data
A UTF-8 plain-text file of _Madame Bovary_ in French from Project Gutenberg. The script performs basic text cleaning to remove Gutenberg-style italics underscores, clean up whitespace line-by-line, and collapse multiple blank lines to normalize line endings. 

Dialogue is identified by two en dashes (e.g. _--Bonjour, monsieur_), while narration is counted as everything else.

## Usage
Run the script from the Terminal using ```python bovary_tense_count.py --txt bovary.txt```.

```fr_core_news_md``` is the French-language model used to identify verbs (```{VERB} and {AUX}```). To specify a different spaCy French model like ```fr_core_news_sm```, you can also optionally specify:

```python bovary_tense_count.py --txt bovary.txt --model fr_core_news_sm```

## Tense labels
Possible spaCy tense labels may include:
```
Label     Meaning
-------------------------------------
Pres      Present
Imp       Imperfect
Past      Past
Fut       Future
UNK       No tense label was provided
```

**Note:** The program counts the morphological tense of finite tokens and so does not directly identify compound tense constructions such as the passé composé or plus-que-parfait, which are also past tense.
 
## Output
```
Input: bovary.txt
Finite verbs counted: narration=10959, dialogue=1572

Tense       Narration   Dialogue        D-N
-------------------------------------------
Fut               117         55        -62
Imp              6218        186      -6032
Past             1844        156      -1688
Pres             2769       1169      -1600
UNK                11          6         -5
```

A negative value in the D-N column means that the tense appears more often in narration in raw counts. A positive value means that it appears more often in dialogue.
