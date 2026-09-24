#!/usr/bin/env python3
"""Flag wordy or unclear writing in text, Markdown, and code comments.

Reports findings by rule ID from references/human-mode.md. It only
flags; a person or agent decides how to rewrite. Expect some false positives.

Usage:
  clank_detector.py FILE...     check files (code files: comments only)
  clank_detector.py -           check text from stdin
Exit code: 0 if clean, 1 if anything was flagged.
"""
import re
import sys
from pathlib import Path

MAX_SENTENCE_WORDS = 35
MAX_COMMENT_RATIO = 0.4

CODE_COMMENT_PREFIX = {
    ".py": "#", ".sh": "#", ".rb": "#", ".yaml": "#", ".yml": "#", ".toml": "#",
    ".js": "//", ".jsx": "//", ".ts": "//", ".tsx": "//", ".go": "//",
    ".rs": "//", ".java": "//", ".kt": "//", ".swift": "//", ".c": "//",
    ".h": "//", ".cpp": "//", ".cs": "//", ".php": "//", ".scala": "//",
}


def words(*terms):
    return r"\b(" + "|".join(terms) + r")\b"


# (rule, pattern, advice). Patterns are case-insensitive.
PROSE_CHECKS = [
    ("P1", words("additionally", "crucial", "delve[sd]?", "delving", "enhance[sd]?",
                 "foster(s|ed|ing)?", "garner(s|ed)?", "intricate", "leverag(e|es|ed|ing)",
                 "pivotal", "robust", "seamless(ly)?", "showcas(e|es|ed|ing)", "tapestry",
                 "testament", "underscor(e|es|ed|ing)", "vibrant", "landscape"),
     "AI vocabulary; use a plain word"),
    ("P2", words("utiliz(e|es|ed|ing)", "facilitat(e|es|ed|ing)", "numerous",
                 "in order to", "due to the fact that", "in the event that", "prior to"),
     "use the plain word"),
    ("P3", words("serves as", "stands as", "boasts"), "just say 'is' or 'has'"),
    ("P4", words("it'?s worth noting( that)?", "it is (important|worth) (to note|noting)( that)?",
                 "basically", "essentially", "at the end of the day", "needless to say"),
     "filler; delete"),
    ("P5", words("could potentially", "might possibly", "may potentially", "arguably"),
     "stacked hedge; hedge once or not at all"),
    ("P6", words("substrate", "nexus", "north star", "flywheel", "paradigm", "bedrock",
                 "linchpin", "cornerstone", "backbone", "game[- ]changer", "synergy"),
     "metaphor; name the literal thing"),
    ("P8", r"\bnot (just|only|merely)\b[^.]*,? but\b", "'not just X, but Y'; state Y"),
    ("P12", r",\s+(ensuring|highlighting|showcasing|reflecting|fostering|underscoring|emphasizing)\b",
     "'-ing' tail; cut or make it a sentence with a fact"),
    ("R7", words("hope this helps", "let me know if", "feel free to", "happy to help"),
     "sign-off; delete"),
    ("R8", words("great question", "you'?re absolutely right", "excellent question",
                 "certainly!", "of course!"),
     "flattery or filler; respond directly"),
    ("S1", "—", "em dash; use a period or comma"),
    ("S6", "[‘’“”]", "curly quote; use a straight quote"),
]

COMMENT_CHECKS = [
    ("C3", r"^\s*(added|changed|fixed|updated|removed|now uses|previously|was changed)\b",
     "history belongs in commit messages"),
    ("C6", r"^\s*(def |class |return\b|import |from \S+ import|if .*[:{]$|for .*[:{]$|"
           r"const |let |var |function\b|\w+\(.*\);?$|\w+ = )",
     "looks like commented-out code; delete it"),
]

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+")


def check_prose(text, where, findings):
    clean = URL.sub("", INLINE_CODE.sub("", text))
    for rule, pattern, advice in PROSE_CHECKS:
        for match in re.finditer(pattern, clean, re.IGNORECASE):
            findings.append((where, rule, f'"{match.group(0).strip()}": {advice}'))
    for sentence in SENTENCE_END.split(clean):
        count = len(sentence.split())
        if count > MAX_SENTENCE_WORDS:
            findings.append((where, "P14", f"{count}-word sentence; split it"))


def check_markdown(lines, path, findings):
    in_fence = False
    for num, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = re.match(r"^#{1,6}\s+(.*)", line)
        if heading:
            title_words = [w for w in heading.group(1).split() if w[:1].isalpha()]
            if len(title_words) >= 3 and all(w[0].isupper() for w in title_words):
                findings.append((f"{path}:{num}", "S4", "title-case heading; use sentence case"))
        check_prose(line, f"{path}:{num}", findings)


def check_code(lines, path, prefix, findings):
    comment_lines = code_lines = 0
    for num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#!"):
            continue
        if stripped.startswith(prefix):
            comment_lines += 1
            text = stripped[len(prefix):].strip()
            where = f"{path}:{num}"
            for rule, pattern, advice in COMMENT_CHECKS:
                if re.search(pattern, text, re.IGNORECASE):
                    findings.append((where, rule, advice))
            check_prose(text, where, findings)
        else:
            code_lines += 1
    total = comment_lines + code_lines
    if total >= 10 and comment_lines / total > MAX_COMMENT_RATIO:
        findings.append((str(path), "C1", f"{comment_lines} of {total} lines are comments; "
                                          "keep only the ones that explain why"))


def check_file(path, findings):
    if str(path) == "-":
        check_markdown(sys.stdin.read().splitlines(), "<stdin>", findings)
        return
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    prefix = CODE_COMMENT_PREFIX.get(path.suffix.lower())
    if prefix:
        check_code(lines, path, prefix, findings)
    else:
        check_markdown(lines, path, findings)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    findings = []
    for arg in argv:
        path = Path(arg)
        if arg != "-" and not path.is_file():
            print(f"not a file: {arg}", file=sys.stderr)
            return 2
        check_file(path, findings)
    for where, rule, message in findings:
        print(f"{where}: [{rule}] {message}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
