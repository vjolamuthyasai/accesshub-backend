import requests
from flask import Blueprint, jsonify, request, send_file

from app.services import generate_pdf
from app.services.axe_checker import run_axe_analysis

main = Blueprint("main", __name__)

@main.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Please provide a URL ?url="}), 400

    try:
       result = run_axe_analysis(url)
       summary = {
           "total_issues": sum(len(v.get("nodes", [])) for v in result.get("violations", [])),
           "by_impact": {}
       }
       for v in result["violations"]:
           impact = v.get("impact", "unknown")
           summary["by_impact"][impact] = summary["by_impact"].get(impact, 0) + 1

       return jsonify({
           "url": url,
           "summary": summary,
           "issues": result["violations"]
       })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/analyze/pdf", methods=["GET"])
def analyze_pdf():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Please provide a URL ?url="}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        report = run_axe_analysis(url)

        pdf_path = generate_pdf(report)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500