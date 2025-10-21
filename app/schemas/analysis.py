from typing import Any, List, Dict
from pydantic import BaseModel

class UploadResponse(BaseModel):
    job_id: str

class AnalysisResult(BaseModel):
    job_id: str
    rows_returned: int
    dataframe_preview: List[Dict[str, Any]] | None
    summary: Dict[str, Dict[str, Any]] | None
    plots: List[str]

class ErrorResponse(BaseModel):
    detail: str
