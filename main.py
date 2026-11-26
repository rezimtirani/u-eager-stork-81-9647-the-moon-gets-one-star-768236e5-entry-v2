"""One-star review of the Moon, corrected edition.

Writes a single line — a one-star review left for the moon — to
$MAKEFUN_OUTPUT_DIR/entry.txt for the make.fun bounty "The Moon Gets
One Star". The moon works the night shift, borrows all its light, and
still gets the poetry; the reviewer works overtime and gets no sonnet.
Only the Python standard library is used.
"""

import os
import sys

LINE = "One star. The moon works nights, steals the sun's light, gets poems — I do overtime and nobody writes me a sonnet."

LIMIT = 120


def check_line(text):
    """Return the review line once it passes the sealed gate, else raise.

    The gate takes UTF-8 text of 1 to 120 characters, not only white
    space, on a single line with no trailing newline. A bad line is
    refused here, loudly, instead of shipping an entry the judge
    never sees.
    """
    if not isinstance(text, str):
        raise TypeError("review line must be text")
    stripped = text.strip()
    if not stripped:
        raise ValueError("review line must not be blank")
    if stripped != text:
        raise ValueError("review line has leading or trailing space")
    if len(stripped) > LIMIT:
        raise ValueError(
            "review line is %d characters, over the %d limit"
            % (len(stripped), LIMIT)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("review must be a single line")
    return stripped


def describe_line(text):
    """Summarise the line for the run log: characters vs UTF-8 bytes.

    The gate measures characters, while the file holds bytes; the em
    dash in this review is one character but three bytes, so the two
    counts are reported side by side to keep the 120-char gate honest.
    """
    encoded = text.encode("utf-8")
    for char in text:
        if ord(char) < 32:
            raise ValueError("review holds a control character: U+%04X" % ord(char))
    return "%d characters, %d UTF-8 bytes" % (len(text), len(encoded))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = check_line(LINE)
    summary = describe_line(line)
    target = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    print("wrote %s (%s)" % (target, summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
