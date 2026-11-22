"""Regenerate Figure 3 directly from the pinned public dashboard data."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE.parents[1] / "page/data/onet.json").read_text())
occupation = next(o for o in data["occupations"] if o["soc"] == "15-1252.00")
activity, weighted = (occupation[k]["ordinal"] for k in ("p", "c"))
phases = data["phases"]
assert len(phases) == len(activity) == len(weighted) == 6
assert all(0 <= w <= a for a, w in zip(activity, weighted))

svg = ["""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" role="img" aria-labelledby="title description">
<title id="title">Software developers: penetration-weighted activity by phase</title>
<desc id="description">Six horizontal bars show the ordinal activity share broken into the portion weighted by published task penetration and its remainder. The figure reports the total weighted share of the activity index.</desc>
<rect width="1000" height="560" fill="white"/>
<g font-family="Arial, sans-serif" fill="#132634">
<text x="32" y="53" font-size="30" font-weight="700">Software developers: AI overlay by phase</text>
<text x="32" y="86" font-size="19">Share of the occupation's modeled activity index</text>
<rect x="32" y="109" width="24" height="18" fill="#13646a"/>
<text x="67" y="124" font-size="17">Weighted by published task penetration</text>
<rect x="475" y="109" width="24" height="18" fill="#cddde3" stroke="#607884"/>
<text x="510" y="124" font-size="17">Remainder of activity index</text>"""]
x0 = 187
scale = 17
for pct in range(0, 41, 10):
    x = x0 + scale * pct
    svg.append(f'<line x1="{x}" x2="{x}" y1="163" y2="452" stroke="#c6d1d5"/>')
    svg.append(f'<text x="{x}" y="477" font-size="16" text-anchor="middle">{pct}%</text>')
for i, (phase, a, w) in enumerate(zip(phases, activity, weighted)):
    y = 174 + i * 46
    svg.append(f'<text x="32" y="{y+22}" font-size="20">{phase.title()}</text>')
    svg.append(f'<rect x="{x0}" y="{y}" width="{a*100*scale:.2f}" height="28" fill="#cddde3" stroke="#607884"/>')
    if w:
        svg.append(f'<rect x="{x0}" y="{y}" width="{w*100*scale:.2f}" height="28" fill="#13646a"/>')
    svg.append(f'<text x="{x0+a*100*scale+10:.2f}" y="{y+20}" font-size="15">{w:.1%} / {a:.1%}</text>')
svg.append(f'<text x="32" y="528" font-size="18" font-weight="700">Weighted total: {sum(weighted):.2%} of the activity index. This is not work time.</text>')
svg.append('</g></svg>')
(HERE / "ai-overlay-developers.svg").write_text("\n".join(svg)+"\n", encoding="utf-8")
