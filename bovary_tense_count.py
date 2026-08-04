'''
This program counts verb tense/aspect distributions in Madame Bovary 
by Gustave Flaubert (French), comparing dialogue with narration.

Input: plain text file of the novel
Output: a table in the Terminal

Usage: bovary_tense_count.py --txt bovary.txt
'''

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import spacy


def normalize_text(raw: str) -> str:
    '''
    Cleans plain-text artifacts from Project Gutenberg using regex.
    '''

    text = raw.replace("\r\n", "\n").replace("\r", "\n")

    # Removes Gutenberg-style italics underscores
    text = re.sub(r"_(\S+)_", r"\1", text)

    # Cleans up whitespace line-by-line and collapses multiple blank lines
    lines = []
    blank_lines_count = 0

    for line in text.split("\n"):
        line = re.sub(r"[ ]{2,}", " ", line.rstrip())
        if line.strip() == "":
            blank_lines_count += 1
            if blank_lines_count <= 1:
                lines.append("")
        else:
            blank_lines_count = 0
            lines.append(line)

    return "\n".join(lines)
    
def main():
    ap = argparse.ArgumentParser(
        description="Tense counts: dialogue vs. narration in Bovary."
    )
    ap.add_argument("--txt", required=True)
    ap.add_argument("--model", default="fr_core_news_md")
    args = ap.parse_args()

    txt_path = Path(args.txt)
    raw = txt_path.read_text(encoding="utf-8", errors="replace")
    text = normalize_text(raw)

    nlp = spacy.load(args.model)

    tense_counts = defaultdict(Counter) 
    totals = Counter()

    dialogue_prefix = re.compile(r"^--\S") # My edition uses "--" for dialogue

    for line in text.split("\n"):
        if not line.strip():
            continue

        reg = "dialogue" if dialogue_prefix.match(line) else "narration"
        if reg == "dialogue":
            line = dialogue_prefix.sub("", line)

        doc = nlp(line)
        for token in doc:
            if token.pos_ not in {"VERB", "AUX"}:
                continue
            if token.morph.get("VerbForm") != ["Fin"]: # Finite verbs only
                continue

            tense = token.morph.get("Tense")
            label = tense[0] if tense else "UNK"
            tense_counts[reg][label] += 1
            totals[reg] += 1

    labels = sorted(set(tense_counts["narration"]) | set(tense_counts["dialogue"]))

    print(f"Input: {txt_path}")
    print(f"Finite verbs counted: narration={totals['narration']}, dialogue={totals['dialogue']}\n")
    print(f"{'Tense':<10} {'Narration':>10} {'Dialogue':>10} {'D-N':>10}")
    print("-" * 44)
    for label in labels:
        n = tense_counts["narration"][label]
        d = tense_counts["dialogue"][label]
        print(f"{label:<10} {n:>10} {d:>10} {d-n:>10}")

if __name__ == "__main__":
    main()
