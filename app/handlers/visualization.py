import os
import uuid
import matplotlib.pyplot as plt
from .base import Handler
import pandas as pd
from urllib.parse import urljoin
from fastapi import Request

PLOT_DIR = "tmp/plots"
BASE_URL = "127.0.0.1:8000"
os.makedirs(PLOT_DIR, exist_ok=True)

class VisualizationHandler(Handler):
    async def handle(self, request) -> dict:
        df = request.get("dataframe")
        if df is None or not isinstance(df, pd.DataFrame):
            return request
        numeric_columns = df.select_dtypes(include=['number']).columns
        plot_paths = []
        if numeric_columns.empty:
            request['plots'] = plot_paths
            print(" No numeric column was found! ")
            return request
        for col in numeric_columns:
            try:
                plt.figure()
                df[col].hist(bins=20)
                plt.title(f"Distribution of {col}")
                plt.xlabel(col)
                plt.ylabel("Frequency")
                filename = f"{uuid.uuid4()}_{col}.png"
                filepath = os.path.join(PLOT_DIR, filename)
                plt.savefig(filepath)
                plt.close()
                url = f"{BASE_URL}/tmp/plots/{filename}"
                plot_paths.append(url)
            except Exception:
                plt.close()
                continue
        request['plots'] = plot_paths
        return request
