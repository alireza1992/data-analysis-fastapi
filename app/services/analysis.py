import uuid
from app.handlers.HANDLER_REGISTRY import HANDLER_REGISTRY
from fastapi import UploadFile, HTTPException
import pandas as pd
import psutil
from pydantic import ValidationError
from app.schemas.validation import FileValidationModel
from app.utils.serialization import to_native
from typing import Any, Dict

# In-memory storage: job_id -> dict result
_data_storage: dict[str, Dict[str, Any]] = {}


class AnalysisService:
    async def analyse_file(self, file: UploadFile) -> str:
        try:
            df = pd.read_csv(file.file, encoding="latin1", on_bad_lines="skip")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {e}")
        try:
            FileValidationModel(
                filename=file.filename,
                size=getattr(file, 'size', 0) or 0,
                available_memory=psutil.virtual_memory().available,
                needed_memory=df.memory_usage(deep=True).sum(),
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        job_id = await self._save_dataset(df)
        return job_id

    async def _save_dataset(self, df: pd.DataFrame) -> str:
        middlewares = ["cleaning", "summary", "visualization"]
        job_id = str(uuid.uuid4())
        request: Dict[str, Any] = {"job_id": job_id, "dataframe": df}
        result = self._run_middlewares(middlewares, request)
        # Ensure dataframe still present
        if 'dataframe' not in result:
            result['dataframe'] = df
        _data_storage[job_id] = result
        return job_id

    def get_dataset(self, job_id: str) -> Dict[str, Any] | None:
        stored = _data_storage.get(job_id)
        if not stored:
            return None
        df = stored.get('dataframe')
        if isinstance(df, pd.DataFrame):
            preview = df.head(5).to_dict(orient='records')
        else:
            preview = None
        summary = stored.get('summary')
        plots = stored.get('plots', [])
        safe_summary = to_native(summary) if summary else None
        safe_preview = to_native(preview) if preview else None
        return {
            'job_id': job_id,
            'rows_returned': len(safe_preview) if safe_preview else 0,
            'dataframe_preview': safe_preview,
            'summary': safe_summary,
            'plots': plots,
        }

    def _run_middlewares(self, middlewares: list[str], request: Dict[str, Any]) -> Dict[str, Any]:
        current = request
        for name in middlewares:
            handler_class = HANDLER_REGISTRY.get(name)
            if not handler_class:
                raise ValueError(f"Unknown handler: {name}")
            result = handler_class().handle(current)
            if result is None:
                raise HTTPException(status_code=500, detail=f"Handler '{name}' returned None")
            if 'dataframe' not in result and 'dataframe' in current:
                result['dataframe'] = current['dataframe']
            current = result
        return current
