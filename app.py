from flask import Flask,request,jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_accessibility(html, url):
    soup = BeautifulSoup(html, "html.parser")
    issues = []

    if not soup.title or not soup.title.string.strip():
        issues.append({
            "type": "missing_title",
            "element": "<title>",
            "description": "Page is missing a title tag",
            "severity": "high"
        })

    images = soup.find_all("img")

    for img in images:
        if not img.get(("alt")):
            issues.append({
                "type": "alt_text_missing",
                "element": str(img)[:80],  # first 80 chars of the img tag
                "description": "Image missing alt attribute",
                "severity": "high"
            })

    headings = [int(h.name[1]) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    for i in range(1, len(headings)):
        if headings[i] - headings[i - 1] > 1:
            issues.append({
                "type": "heading_structure",
                "element": f"h{headings[i]}",
                "description": f"Improper heading order: h{headings[i - 1]} → h{headings[i]}",
                "severity": "medium"
            })

    # Build summary
    summary = {
        "total_issues": len(issues),
        "high": sum(1 for i in issues if i["severity"] == "high"),
        "medium": sum(1 for i in issues if i["severity"] == "medium"),
        "low": sum(1 for i in issues if i["severity"] == "low"),
    }

    return {
        "url": url,
        "issues": issues,
        "summary": summary
    }


@app.route("/analyze", methods= ["GET"])
def analyze():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "Please provide a URL ?url="}),400
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        report = check_accessibility(response.text, url)
        return jsonify(report)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug = True)
