from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Create the FastAPI app instance
app = FastAPI(title="SEO Reporting Agent", description="Agent for generating SEO reports")

class ReportRequest(BaseModel):
    audit_data: dict
    format: str = "markdown"

@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    # Placeholder implementation - will be implemented in Task 5
    return {
        "report_content": "This is a placeholder report. Implementation coming in Task 5.",
        "format": request.format
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SEO Reporting Agent"}