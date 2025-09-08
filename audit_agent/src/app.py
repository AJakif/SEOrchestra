from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio

from shared.src.schemas import AuditResult, AuditItem
from .core.crawler import WebsiteCrawler
from .core.seo_checks import SEOChecker

app = FastAPI(title="SEO Audit Agent", description="Agent for performing technical SEO audits")

class AuditRequest(BaseModel):
    url: str
    max_pages: int = 10

@app.post("/crawl-and-audit")
async def crawl_and_audit(request: AuditRequest):
    try:
        # Initialize crawler and SEO checker
        crawler = WebsiteCrawler(max_pages=request.max_pages)
        seo_checker = SEOChecker()
        
        # Crawl the website
        pages_content = await crawler.crawl(request.url)
        
        # Run SEO checks on each page
        all_issues = []
        for url, html in pages_content.items():
            page_issues = seo_checker.run_all_checks(html, url)
            all_issues.extend(page_issues)
        
        # Count issues by severity
        severity_count = {
            "critical": len([i for i in all_issues if i.severity == "critical"]),
            "error": len([i for i in all_issues if i.severity == "error"]),
            "warning": len([i for i in all_issues if i.severity == "warning"]),
            "info": len([i for i in all_issues if i.severity == "info"]),
        }
        
        # Prepare the response
        audit_result = AuditResult(
            base_url=request.url,
            total_issues=len(all_issues),
            issues_by_severity=severity_count,
            items=all_issues
        )
        
        return audit_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SEO Audit Agent"}