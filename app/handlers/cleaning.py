import pandas as pd
from .base import Handler


class CleaningHandler(Handler):
    async def handle(self, request):
        df = request.get("dataframe")
        if df is None or not isinstance(df, pd.DataFrame):
            return request
        df = df.dropna()
        df = df.drop_duplicates()
        df = df.select_dtypes(include=['number', 'object', 'category', 'bool', 'datetime', 'timedelta'])
        df = df.replace("''", 'Unknown')
        request["dataframe"] = df
        return request