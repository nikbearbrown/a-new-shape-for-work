"""One title normaliser shared by the O*NET title map (Mac) and the posting extractor (cluster). Stdlib only.

"Senior Software Engineer II - Payments (Remote)" -> "software engineer"
Lower-case; '&' -> 'and'; drop bracketed text; cut at the first ' - ', ' | ', ' – ', ',' or ' / ' that follows a
word; drop work-mode words; drop level words at either end (senior, sr, junior, jr, lead, principal, staff, entry
level, mid level, roman numerals, level N, a trailing digit). "Associate" is kept: it is part of many real titles.
"""
import re

LEVEL_EDGE = {"senior", "sr", "junior", "jr", "lead", "principal", "staff", "entry", "entry-level", "mid", "mid-level",
              "level", "i", "ii", "iii", "iv", "v", "1", "2", "3", "4", "5", "experienced", "new", "grad", "graduate"}
MODE = re.compile(r"\b(remote|hybrid|onsite|on-site|in-office|full[- ]time|part[- ]time|per diem|prn|contract|temporary|temp)\b")
CUT = re.compile(r"\s+[-–—|/]\s+|,|\s+at\s+|\s+@\s+")


def norm_title(t):
    t = (t or "").lower().replace("&", " and ")
    t = re.sub(r"\(.*?\)|\[.*?\]", " ", t)
    t = CUT.split(t, maxsplit=1)[0]
    t = MODE.sub(" ", t)
    t = re.sub(r"[^a-z0-9+#.' -]", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" .-'")
    words = t.split()
    while words and words[0] in LEVEL_EDGE:
        words.pop(0)
    while words and words[-1] in LEVEL_EDGE:
        words.pop()
    return " ".join(words)
