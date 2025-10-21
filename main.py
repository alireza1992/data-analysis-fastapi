from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.api.routes.analysis import router as analysis_router

app = FastAPI(
    title="File Analysis API",
    description="API for uploading and on-demand analyze csv files.",
    version="1.0.0"
)

app.include_router(analysis_router, prefix="/api/v1")

app.mount("/tmp", StaticFiles(directory="tmp"), name="tmp")