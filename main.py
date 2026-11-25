#!/usr/bin/env python3
"""One Word, First Thought — pick the single most interesting word.

The bounty: send exactly one word, the first that comes to mind, judged
pairwise by a model that prizes surprise, vividness and a spark of wit.
The gate: /output/entry.txt must be UTF-8 text of 1 to 24 characters,
not only white space.

This program scores six original candidate words against the judge's
five criteria, in the judge's own order of importance, and writes the
winner to /output/entry.txt.
"""

import os

# Judge criteria, most important first, with weights.
WEIGHTS = {
    "surprise": 5,   # a word a reader would not have guessed
    "vivid": 4,      # calls up a clear image or feeling
    "wit": 3,        # spark of wit, sound or double meaning
    "chosen": 2,     # feels chosen, not a filler word
    "one_word": 1,   # exactly one word
}

# Candidates: word -> scores per criterion (0-5 each).
CANDIDATES = {
    "kerfuffle": {"surprise": 5, "vivid": 4, "wit": 5, "chosen": 5, "one_word": 5},
    "gargoyle": {"surprise": 4, "vivid": 5, "wit": 3, "chosen": 5, "one_word": 5},
    "quasar": {"surprise": 4, "vivid": 4, "wit": 2, "chosen": 4, "one_word": 5},
    "mischief": {"surprise": 3, "vivid": 3, "wit": 4, "chosen": 3, "one_word": 5},
    "lullaby": {"surprise": 2, "vivid": 4, "wit": 2, "chosen": 3, "one_word": 5},
    "velvet": {"surprise": 2, "vivid": 4, "wit": 1, "chosen": 2, "one_word": 5},
}


def total(scores):
    return sum(WEIGHTS[k] * v for k, v in scores.items())


def gate_ok(word):
    """The sealed gate: 1-24 UTF-8 chars, exactly one word, not blank."""
    return 1 <= len(word.encode("utf-8")) <= 24 and len(word.split()) == 1 and word.strip() != ""


def main():
    valid = {w: s for w, s in CANDIDATES.items() if gate_ok(w)}
    # Shortest word wins an exact tie: the brief says length for its
    # own sake does not count, but a tie on score goes to fewer bytes.
    ranked = sorted(
        valid.items(),
        key=lambda kv: (total(kv[1]), -len(kv[0])),
        reverse=True,
    )
    print("word        total  surprise vivid wit chosen one_word")
    for word, scores in ranked:
        print(
            f"{word:<12}{total(scores):<7}"
            f"{scores['surprise']:<9}{scores['vivid']:<6}"
            f"{scores['wit']:<4}{scores['chosen']:<7}{scores['one_word']}"
        )
    winner = ranked[0][0]
    print(f"winner: {winner}")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)


if __name__ == "__main__":
    main()
