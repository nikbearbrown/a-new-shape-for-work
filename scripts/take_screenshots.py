"""Save PNG screenshots of the prototype page, one per chart section, to docs/screenshots/.

Serve the page first, then run this:
    python3 -m http.server -d page 8765
    python3 -I scripts/take_screenshots.py [URL]     # default http://localhost:8765/
Needs Playwright for Python with its Chromium (pip install playwright; playwright install chromium).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8765/"
OUT = Path(__file__).resolve().parents[1] / "docs/screenshots"
SECTIONS = [("s-profile", "chart-1-phase-profile"), ("s-cal", "calibration"), ("s-tasks", "chart-7-day-to-day"),
            ("s-family", "chart-9-job-family"), ("s-ladder", "chart-3-seniority-ladder"),
            ("s-stack", "chart-5-requirement-stack"), ("s-exp", "chart-4-experience"), ("s-bump", "chart-6-rank-changes"),
            ("s-shift", "chart-2-phase-shift"), ("s-ai", "chart-8-ai-overlay")]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2, color_scheme="light")
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2500)  # let the D3 charts finish drawing
        top = page.evaluate("document.getElementById('s-profile').getBoundingClientRect().top + window.scrollY")
        page.screenshot(path=OUT / "overview.png", clip={"x": 0, "y": 0, "width": 1280, "height": top}, full_page=True)
        for sid, name in SECTIONS:
            el = page.locator(f"#{sid}")
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            el.screenshot(path=OUT / f"{name}.png")
        browser.close()
    if errors:
        sys.exit("console errors: " + "; ".join(errors))
    print("wrote", len(SECTIONS) + 1, "screenshots to", OUT)


if __name__ == "__main__":
    main()
