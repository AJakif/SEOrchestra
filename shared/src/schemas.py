from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class AuditItem(BaseModel):
    """Represents a single SEO issue found during audit"""
    check_name: str = Field(..., description="Name of the SEO check performed")
    severity: SeverityLevel = Field(..., description="Severity level of the issue")
    description: str = Field(..., description="Human-readable description of the issue")
    found_url: str = Field(..., description="URL where the issue was found")
    recommendation: str = Field(..., description="Recommended fix for the issue")
    context: Optional[dict] = Field(default=None, description="Additional context data")

class AuditResult(BaseModel):
    """Container for all audit findings for a website"""
    base_url: str = Field(..., description="The base URL that was audited")
    audit_timestamp: datetime = Field(default_factory=datetime.now, description="When the audit was performed")
    total_issues: int = Field(..., description="Total number of issues found")
    issues_by_severity: dict = Field(..., description="Count of issues by severity level")
    items: List[AuditItem] = Field(..., description="List of all audit findings")
    
    class Config:
        # Allow using enum values in JSON
        use_enum_values = True

class ReportRequest(BaseModel):
    """Request format for generating a report from audit data"""
    audit_data: AuditResult = Field(..., description="The audit findings to generate a report from")
    format: str = Field("markdown", description="Output format for the report")

class ReportResponse(BaseModel):
    """Response format for generated reports"""
    report_content: str = Field(..., description="The generated report content")
    format: str = Field(..., description="Format of the report content")