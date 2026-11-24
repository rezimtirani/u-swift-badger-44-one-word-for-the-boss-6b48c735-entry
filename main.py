"""One Word for the Boss — the entrypoint.

The bounty asks for exactly one word describing a boss: no phrase,
no caption, no explanation. This program writes that one word to the
output directory, where the sealed scorer reads it.

The word is chosen once, at the top of this file, and the program only
checks it still obeys the gate (one token, 1 to 30 characters) before
writing it out. Nothing is read from the network, from git history,
or from any file outside this repository.
"""

import os
import sys

WORD = "Hoverlord"
GATE_MIN = 1
GATE_MAX = 30


def single_word_ok(word):
    """True when the word is one token inside the gate's length limits."""
    if not isinstance(word, str):
        return False
    if not (GATE_MIN <= len(word) <= GATE_MAX):
        return False
    if word != word.strip():
        return False
    return len(word.split()) == 1


def word_report(word):
    """A short human-readable summary of the word being entered."""
    lines = [
        "word: %s" % word,
        "length: %d characters" % len(word),
        "tokens: %d" % len(word.split()),
        "gate: %d-%d characters, single token" % (GATE_MIN, GATE_MAX),
    ]
    return "\n".join(lines)


def output_path():
    """Resolve the writable output directory the grader provides."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def main():
    if not single_word_ok(WORD):
        print("entry word fails the gate", file=sys.stderr)
        return 1
    path = output_path()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(WORD)
    print(word_report(WORD))
    print("wrote %d characters to %s" % (len(WORD), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
