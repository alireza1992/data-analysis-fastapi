import uuid
from handlers.HANDLER_REGISTRY import HANDLER_REGISTRY
from fastapi import UploadFile, HTTPException
import pandas as pd
import psutil
from pandas.core.interchange.dataframe_protocol import DataFrame
from pydantic import ValidationError
from services.validation import FileValidationModel

# In-memory storage for simplicity (replace with DB in production)
data_storage: dict[str, pd.DataFrame] = {}


class AnalysisService:
    async def analyse_file(self, file: UploadFile):
        df = pd.read_csv(file.file, encoding="latin1", on_bad_lines="skip")
        try:
            FileValidationModel(
                filename=file.filename,
                size=file.size,
                available_memory=psutil.virtual_memory().available,
                needed_memory=df.memory_usage(deep=True).sum()
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        job_id = await self.save_dataset(df)
        return job_id

    @staticmethod
    async def save_dataset(df: DataFrame) -> str:
        middlewares = ['summary', 'cleaning']
        job_id = str(uuid.uuid4())
        request = {"job_id": job_id, "dataframe": df}
        result = AnalysisService.run_middlewares(middlewares, request)
        data_storage[job_id] = result
        return job_id

    @staticmethod
    def get_dataset(job_id: str) -> pd.DataFrame | None:
        raw_df = data_storage.get(job_id)
        return {'cleaned_dataframe': raw_df['dataframe'], 'summary': raw_df['summary']} if raw_df else None

    @staticmethod
    def run_middlewares(middlewares: list, request: dict):
        result = None
        if not middlewares:
            raise ValueError("No middlewares provided")
        for middleware in reversed(middlewares):
            handler_class = HANDLER_REGISTRY.get(middleware)
            if not handler_class:
                raise ValueError(f"Unknown handler: {middleware}")
            result = handler_class().handle(request)
            if result is None:
                raise HTTPException(status_code=500, detail="Error processing the dataset.")

        return result
