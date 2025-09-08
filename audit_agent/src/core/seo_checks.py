from bs4 import BeautifulSoup
from typing import List, Dict, Any
from urllib.parse import urlparse
from shared.src.schemas import AuditResult, AuditItem , SeverityLevel
import time

class SEOChecker:
    def __init__(self):
        pass
        
    def check_title(self, soup: BeautifulSoup, url: str) -> List[AuditItem]:
        issues = []
        title = soup.find('title')
        
        if not title or not title.get_text().strip():
            issues.append(AuditItem(
                check_name="Missing Title Tag",
                severity=SeverityLevel.ERROR,
                description="Page is missing a title tag",
                found_url=url,
                recommendation="Add a descriptive title tag between 50-60 characters"
            ))
        elif len(title.get_text()) > 60:
            issues.append(AuditItem(
                check_name="Title Too Long",
                severity=SeverityLevel.WARNING,
                description=f"Title tag is {len(title.get_text())} characters (recommended: 50-60)",
                found_url=url,
                recommendation="Shorten the title tag to under 60 characters"
            ))
        elif len(title.get_text()) < 50:
            issues.append(AuditItem(
                check_name="Title Too Short",
                severity=SeverityLevel.INFO,
                description=f"Title tag is {len(title.get_text())} characters (recommended: 50-60)",
                found_url=url,
                recommendation="Consider making the title more descriptive"
            ))
            
        return issues
        
    def check_meta_description(self, soup: BeautifulSoup, url: str) -> List[AuditItem]:
        issues = []
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc or not meta_desc.get('content', '').strip():
            issues.append(AuditItem(
                check_name="Missing Meta Description",
                severity=SeverityLevel.WARNING,
                description="Page is missing a meta description",
                found_url=url,
                recommendation="Add a compelling meta description between 150-160 characters"
            ))
        elif meta_desc and len(meta_desc.get('content', '')) > 160:
            issues.append(AuditItem(
                check_name="Meta Description Too Long",
                severity=SeverityLevel.WARNING,
                description=f"Meta description is {len(meta_desc.get('content', ''))} characters (recommended: 150-160)",
                found_url=url,
                recommendation="Shorten the meta description to under 160 characters"
            ))
            
        return issues
        
    def check_headings(self, soup: BeautifulSoup, url: str) -> List[AuditItem]:
        issues = []
        h1s = soup.find_all('h1')
        
        if len(h1s) == 0:
            issues.append(AuditItem(
                check_name="Missing H1 Heading",
                severity=SeverityLevel.ERROR,
                description="Page is missing an H1 heading",
                found_url=url,
                recommendation="Add a single H1 heading that describes the page content"
            ))
        elif len(h1s) > 1:
            issues.append(AuditItem(
                check_name="Multiple H1 Headings",
                severity=SeverityLevel.WARNING,
                description=f"Page has {len(h1s)} H1 headings (recommended: 1)",
                found_url=url,
                recommendation="Use only one H1 heading per page for better SEO"
            ))
            
        return issues
        
    def check_images(self, soup: BeautifulSoup, url: str) -> List[AuditItem]:
        issues = []
        images = soup.find_all('img')
        
        for img in images:
            if not img.get('alt'):
                issues.append(AuditItem(
                    check_name="Missing Alt Text",
                    severity=SeverityLevel.WARNING,
                    description="Image is missing alt text",
                    found_url=url,
                    recommendation="Add descriptive alt text to all images for accessibility and SEO"
                ))
                break  # Only report once per page
                
        return issues
        
    def check_links(self, soup: BeautifulSoup, url: str) -> List[AuditItem]:
        # This is a placeholder - we'll implement proper link checking later
        return []
        
    def run_all_checks(self, html: str, url: str) -> List[AuditItem]:
        soup = BeautifulSoup(html, 'html.parser')
        all_issues = []
        
        # Run all checks
        all_issues.extend(self.check_title(soup, url))
        all_issues.extend(self.check_meta_description(soup, url))
        all_issues.extend(self.check_headings(soup, url))
        all_issues.extend(self.check_images(soup, url))
        all_issues.extend(self.check_links(soup, url))
        
        return all_issues