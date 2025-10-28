from typing import Annotated
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.analysis import AnalysisService
from app.schemas.analysis import UploadResponse, AnalysisResult, ErrorResponse

router = APIRouter()
service = AnalysisService()


@router.post('/upload', response_model=UploadResponse)
async def upload_file(file: Annotated[UploadFile, File()]):
    job_id = service.save(file)
    return UploadResponse(job_id=job_id)


@router.get('/analyse/{job_id}', response_model=AnalysisResult | ErrorResponse)
async def analyser(job_id: str):
    result = await service.analyze(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result
