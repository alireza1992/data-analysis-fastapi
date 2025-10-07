import pandas as pd
from .base import Handler

class SummaryHandler(Handler):
    def handle(self, request) -> dict:
        df = pd.DataFrame(request['dataframe'])  # Ensure df is a DataFrame
        summary = df.describe().to_dict()
        print("[SummaryHandler] Generated summary statistics")

        request['summary'] = summary  # Update the request with the summary

        return request  # Notice: returns dict instead of DataFrame
