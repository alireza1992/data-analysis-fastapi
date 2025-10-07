from typing import Annotated
from services.analysis import AnalysisService
from fastapi import APIRouter
from fastapi import File, UploadFile

router = APIRouter()

analyserService = AnalysisService()


@router.post('/upload')
async def upload_file(file: Annotated[UploadFile, File()]):
    result = await analyserService.analyse_file(file)
    return {"Result": result}


@router.get('/analyse/{job_id}')
async def analyser(job_id: str):
    return {"result": analyserService.get_dataset(job_id)}
