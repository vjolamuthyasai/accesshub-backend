import json
from pathlib import Path
from playwright.sync_api import sync_playwright

AXE_JS_PATH = Path(__file__).parent / "axe.min.js"


def run_axe_analysis(url: str) -> dict:

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Inject axe-core
        axe_script = AXE_JS_PATH.read_text(encoding="utf-8")
        page.add_script_tag(content=axe_script)

        # Run axe
        result = page.evaluate("""async () => {
            return await axe.run();
        }""")

        browser.close()

    return result
