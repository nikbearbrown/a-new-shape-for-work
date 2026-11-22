"""Lexicon surface forms -> data/lexicon-forms.json: lowercased form -> [id, preferred_name, kind, top_class].

    python3 -I scripts/export_lexicon_forms.py [PATH_TO_SKILLS_LEXICON_CHECKOUT]
The prototype used github.com/nikbearbrown/skills-lexicon at main 0ba8e0c2 (3,754 entries)."""
import json, os, sys
from pathlib import Path
_lex = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SKILLS_LEXICON")
if not _lex:
    sys.exit("usage: export_lexicon_forms.py PATH_TO_SKILLS_LEXICON_CHECKOUT (or set SKILLS_LEXICON)")
LEX = Path(_lex)
sys.path.insert(0, str(LEX / "tools"))
import lexicon as L
entries, errs = L.load(LEX / "entries")
out = {}
for e in entries:
    for lab in L.forms(e):
        lab = lab["label"] if isinstance(lab, dict) else lab
        out.setdefault(lab.strip().lower(), [e["id"], e["preferred_name"], e.get("kind"), L.top_class(e)])
Path(__file__).resolve().parents[1].joinpath("data/lexicon-forms.json").write_text(json.dumps(out))
print(len(entries), "entries", len(out), "forms", len(errs), "load errors")
