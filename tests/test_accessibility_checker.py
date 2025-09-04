from app.services import check_accessibility


def test_missing_title():
    html = "<html><body><h1>Heading</h1></body></html>"
    report  = check_accessibility(html, "http://test.com")
    issue_types = [i["type"] for i in report["issues"]]
    assert "missing_title" in issue_types
    assert report["summary"]["high"] == 1


def test_img_without_alt():
    html = "<html><head><title>Test</title></head><body><img src='logo.png'></body></html>"
    report = check_accessibility(html, "http://test.com")
    issue_types = [i["type"] for i in report["issues"]]
    assert "alt_text_missing" in issue_types
    assert report["summary"]["high"] == 1

def test_heading_structure():
    html = "<html><head><title>Test</title></head><body><h1>Title</h1><h3>Sub</h3></body></html>"
    report = check_accessibility(html, "http://test.com")
    issue_types = [i["type"] for i in report["issues"]]
    assert "heading_structure" in issue_types
    assert report["summary"]["medium"] == 1

def test_clean_page():
    html = "<html><head><title>Good</title></head><body><h1>Title</h1><h2>Sub</h2><img src='a.png' alt='ok'></body></html>"
    report = check_accessibility(html, "http://test.com")
    assert report["summary"]["total_issues"] == 0