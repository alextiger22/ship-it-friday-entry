#!/usr/bin/env python3
"""Ship It Friday - make.fun entry.

Writes a single-line git commit message to /output/entry.txt.

v3: after writing, main() reads the file back as bytes and asserts they
equal ENTRY encoded as UTF-8 exactly (no trailing newline, no extra bytes).
"""

import os

ENTRY = "Merge branch 'it-works-on-my-machine' into main. Deploying Friday at 5 PM because the tests passed once."

MAX_CHARS = 159


def _validate(text):
    """Enforce the competition gates: UTF-8, 1-159 chars, not only whitespace.

    Stricter v2 checks: no leading/trailing whitespace, no control
    characters or carriage returns, and the text must survive a UTF-8
    encode/decode round-trip unchanged.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    encoded = text.encode("utf-8")  # raises UnicodeEncodeError on bad data
    if encoded.decode("utf-8") != text:
        raise ValueError("entry does not survive a UTF-8 round-trip")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\r" in text:
        raise ValueError("entry must not contain carriage returns")
    if any(ord(ch) < 0x20 and ch != "\n" for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def main():
    line = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(line)
    # v3 read-back self-verification: the bytes on disk must be exactly
    # ENTRY encoded as UTF-8, with no trailing newline or extra bytes.
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        raise ValueError("read-back verification failed: /output/entry.txt "
                         "does not match ENTRY exactly")


if __name__ == "__main__":
    main()
