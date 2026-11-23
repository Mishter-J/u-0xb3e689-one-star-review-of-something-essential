#!/usr/bin/env python3
"""One-Star Review of Something Essential — make.fun entry.

Writes a single deadpan one-star review of sleep (100 characters,
one line) to /output/entry.txt.

Deterministic: the review is a fixed string constant. No randomness,
no clock, no network, no input files. Running this program twice
produces byte-identical output. After writing, the program reads the
file back and verifies the bytes match the review exactly, so a
truncated or mangled write can never pass silently.
"""

import os

# Gate limits from the competition rules: a single-line review of
# 1 to 160 characters. The judge's brief also forbids exclamation
# marks doing the work, so the review must not contain one.
MAX_REVIEW_CHARS = 160
MIN_REVIEW_CHARS = 1
FORBIDDEN_CHARS = "!"

REVIEW = (
    "Sleep takes eight hours a night and I still wake up tired. "
    "Worst subscription I never signed up for."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(review: str) -> None:
    """Check the review against the gate before writing anything."""
    if not MIN_REVIEW_CHARS <= len(review) <= MAX_REVIEW_CHARS:
        raise ValueError(
            f"review must be {MIN_REVIEW_CHARS}-{MAX_REVIEW_CHARS} "
            f"characters, got {len(review)}"
        )
    if "\n" in review or "\r" in review:
        raise ValueError("review must be a single line")
    if not review.strip():
        raise ValueError("review must not be only whitespace")
    for ch in FORBIDDEN_CHARS:
        if ch in review:
            raise ValueError(f"review must not contain {ch!r}")


def write_review(review: str) -> None:
    """Write the review and verify the bytes on disk match exactly."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(review)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != review.encode("utf-8"):
        raise RuntimeError("verification failed: output bytes differ")


def main() -> None:
    validate(REVIEW)
    write_review(REVIEW)
    print(f"Wrote {len(REVIEW)} characters to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
