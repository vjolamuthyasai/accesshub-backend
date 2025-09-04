from bs4 import BeautifulSoup


def check_accessibility(html, url):
    soup = BeautifulSoup(html, "html.parser")
    issues = []

    # 1. Page title check
    if not soup.title or not soup.title.string.strip():
        issues.append({
            "type": "missing_title",
            "element": "<title>",
            "description": "Page is missing a title tag",
            "severity": "high"
        })

    # 2. Images without alt
    images = soup.find_all("img")
    for img in images:
        if not img.get("alt"):
            issues.append({
                "type": "alt_text_missing",
                "element": str(img)[:80],
                "description": "Image missing alt attribute",
                "severity": "high"
            })

    # 3. Heading structure check
    headings = [int(h.name[1]) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    for i in range(1, len(headings)):
        if headings[i] - headings[i - 1] > 1:
            issues.append({
                "type": "heading_structure",
                "element": f"h{headings[i]}",
                "description": f"Improper heading order: h{headings[i-1]} → h{headings[i]}",
                "severity": "medium"
            })

    summary = {
        "total_issues": len(issues),
        "high": sum(1 for i in issues if i["severity"] == "high"),
        "medium": sum(1 for i in issues if i["severity"] == "medium"),
        "low": sum(1 for i in issues if i["severity"] == "low"),
    }

    return {"url": url, "issues": issues, "summary": summary}
