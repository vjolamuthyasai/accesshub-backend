import requests
from flask import Blueprint, jsonify, request, send_file

from app.services import check_accessibility,generate_pdf


main = Blueprint("main", __name__)

@main.route("/analyze", methods=["GET"])
def analyze():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Please provide a URL ?url="}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        report = check_accessibility(response.text, url)
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/analyze/pdf", methods=["GET"])
def analyze_pdf():
    def analyze_pdf():
        url = request.args.get("url")
        if not url:
            return jsonify({"error": "Please provide a URL ?url="}), 400

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            report = check_accessibility(response.text, url)

            pdf_path = generate_pdf(report)
            return send_file(pdf_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500