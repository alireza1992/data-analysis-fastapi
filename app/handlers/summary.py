import pandas as pd
from .base import Handler
from app.utils.serialization import to_native

class SummaryHandler(Handler):
    def handle(self, request) -> dict:
        df = request.get('dataframe')
        if df is None or not isinstance(df, pd.DataFrame):
            return request
        try:
            desc = df.describe()
        except Exception:
           return None
        raw_summary = desc.to_dict()
        summary = to_native(raw_summary)
        request['summary'] = summary
        return request
