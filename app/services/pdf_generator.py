from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(report, filename="accessibility_report.pdf"):
    """
    Generate a PDF accessibility report.
    :param report: dict from check_accessibility()
    :param filename: output file name
    :return: path to the saved PDF
    """
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=letter)

    story = []
    story.append(Paragraph(f"Accessibility Report for {report['url']}", styles["Title"]))
    story.append(Spacer(1, 12))

    # Summary
    summary = report["summary"]
    story.append(Paragraph("Summary:", styles["Heading2"]))
    story.append(Paragraph(f"Total Issues: {summary['total_issues']}", styles["Normal"]))
    story.append(Paragraph(f"High: {summary['high']}, Medium: {summary['medium']}, Low: {summary['low']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Issues
    story.append(Paragraph("Issues:", styles["Heading2"]))
    for issue in report["issues"]:
        story.append(Paragraph(f"- [{issue['severity'].upper()}] {issue['description']}", styles["Normal"]))
        story.append(Paragraph(f"  Element: {issue['element']}", styles["Code"]))
        story.append(Spacer(1, 6))

    doc.build(story)

    return os.path.abspath(filename)
