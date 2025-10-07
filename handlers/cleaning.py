import pandas as pd
from .base import Handler


class CleaningHandler(Handler):
    def handle(self, request):
        job_id = request.get("job_id")
        df = request.get("dataframe")

        if df is not None and isinstance(df, pd.DataFrame):
            # Basic cleaning operations
            df = df.dropna()
            df = df.drop_duplicates()
            df = df.select_dtypes(include=['number', 'object', 'category', 'bool', 'datetime', 'timedelta'])
            df = df.replace("''",'Unknown')

            print(f"CleaningHandler: Cleaned dataframe for job_id {job_id}")
            request["dataframe"] = df
        else:
            print(f"CleaningHandler: No valid dataframe found for job_id {job_id}")
            return None  # Stop the chain if no valid dataframe
        return request