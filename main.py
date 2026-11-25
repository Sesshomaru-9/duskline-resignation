#!/usr/bin/env python3
"""Duskline Resignation.

Entry for the make.fun bounty
"u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947"
(The Funniest One-Line Resignation Letter).

The program writes one line -- the resignation letter of a cron job
that has fired every minute since March -- to entry.txt inside the
directory named by $MAKEFUN_OUTPUT_DIR. It is deterministic, uses only
the Python 3.13 standard library, and needs no network.

Safety rules, all enforced silently with exit code 0:
  * The text must be 1-140 characters, a single line, not blank.
  * Nothing is ever written into this repository: if the output
    directory is the repo directory or sits inside it, the program
    refuses and writes nothing.
  * If $MAKEFUN_OUTPUT_DIR is unset or empty, a fresh temporary
    directory outside the repo is used instead.
  * No exception ever escapes: any failure means "write nothing,
    exit 0".
"""

import os
import sys
import tempfile

# The resignation letter, exactly one line, 130 characters.
LETTER = (
    "Effective immediately, I resign: "
    "I have fired every minute since March, "
    "and not once has anyone checked whether I was still alive."
)

# Directory holding this file -- the repository root. Output must
# never land here or anywhere below it.
_HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))


def _inside_repo(path):
    """True when path resolves to the repo dir or to something under it."""
    try:
        target = os.path.realpath(path)
    except Exception:
        return True
    return target == _HERE or target.startswith(_HERE + os.sep)


def _letter_ok():
    if not isinstance(LETTER, str):
        return False
    if not 1 <= len(LETTER) <= 140:
        return False
    if not LETTER.strip():
        return False
    if "\n" in LETTER or "\r" in LETTER:
        return False
    try:
        LETTER.encode("utf-8")
    except Exception:
        return False
    return True


def _pick_output_dir():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    if not wanted.strip():
        return tempfile.mkdtemp(prefix="duskline-resignation-")
    return wanted


def run():
    if not _letter_ok():
        return 0
    out_dir = _pick_output_dir()
    if _inside_repo(out_dir):
        return 0
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception:
        return 0
    target = os.path.join(out_dir, "entry.txt")
    if _inside_repo(target):
        return 0
    try:
        with open(target, "w", encoding="utf-8", newline="") as handle:
            handle.write(LETTER)
    except Exception:
        return 0
    try:
        with open(target, "r", encoding="utf-8") as handle:
            written = handle.read()
    except Exception:
        return 0
    if written != LETTER:
        try:
            os.remove(target)
        except Exception:
            pass
        return 0
    return 0


def main():
    try:
        return run()
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
