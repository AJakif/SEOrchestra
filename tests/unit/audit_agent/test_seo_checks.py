import pytest
from bs4 import BeautifulSoup
from audit_agent.src.core.seo_checks import SEOChecker
from shared.src.schemas import SeverityLevel

def test_check_title_missing():
    """Test detection of missing title tag"""
    html = "<html><head></head><body></body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    checker = SEOChecker()
    
    issues = checker.check_title(soup, "https://example.com")
    assert len(issues) == 1
    assert issues[0].severity == SeverityLevel.ERROR
    assert "Missing Title Tag" in issues[0].check_name

def test_check_title_too_long():
    """Test detection of title that's too long"""
    html = "<html><head><title>This is a very long title that exceeds the recommended character limit of 60 characters</title></head><body></body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    checker = SEOChecker()
    
    issues = checker.check_title(soup, "https://example.com")
    assert len(issues) == 1
    assert issues[0].severity == SeverityLevel.WARNING
    assert "Title Too Long" in issues[0].check_name

def test_check_meta_description_missing():
    """Test detection of missing meta description"""
    html = "<html><head></head><body></body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    checker = SEOChecker()
    
    issues = checker.check_meta_description(soup, "https://example.com")
    assert len(issues) == 1
    assert issues[0].severity == SeverityLevel.WARNING
    assert "Missing Meta Description" in issues[0].check_name

def test_check_headings_missing_h1():
    """Test detection of missing H1 heading"""
    html = "<html><body><h2>Subheading</h2></body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    checker = SEOChecker()
    
    issues = checker.check_headings(soup, "https://example.com")
    assert len(issues) == 1
    assert issues[0].severity == SeverityLevel.ERROR
    assert "Missing H1 Heading" in issues[0].check_name

def test_check_images_missing_alt():
    """Test detection of images missing alt text"""
    html = '<html><body><img src="image.jpg"></body></html>'
    soup = BeautifulSoup(html, 'html.parser')
    checker = SEOChecker()
    
    issues = checker.check_images(soup, "https://example.com")
    assert len(issues) == 1
    assert issues[0].severity == SeverityLevel.WARNING
    assert "Missing Alt Text" in issues[0].check_name

def test_run_all_checks():
    """Test running all checks on HTML with multiple issues"""
    html = """
    <html>
        <head>
            <title>A title that is way too long and exceeds the recommended character limit</title>
        </head>
        <body>
            <img src="image.jpg">
            <h2>Subheading but no H1</h2>
        </body>
    </html>
    """
    checker = SEOChecker()
    
    issues = checker.run_all_checks(html, "https://example.com")
    # Should find at least 3 issues: long title, missing alt, missing H1
    assert len(issues) >= 3