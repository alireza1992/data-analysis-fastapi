from fastapi import FastAPI
from routes.analysis import router as analysis_router

app = FastAPI(
    title="File Analysis API",
    description="API for uploading and on-demand analyze csv files.",
    version="1.0.0"
)

app.include_router(analysis_router, prefix="/api/v1")
