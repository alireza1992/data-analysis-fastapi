import os
import uuid
import matplotlib.pyplot as plt
from .base import Handler

PLOT_DIR = "tmp/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

class VisualizationHandler(Handler):
    def handle(self, request) -> dict:
        plot_paths = []
        df = request.get("dataframe")

        numeric_columns = df.select_dtypes(include=['number']).columns

        if numeric_columns.empty:
            print("[VisualizationHandler] No numeric columns found.")
            return {"plots": []}

        for col in numeric_columns:
            plt.figure()
            df[col].hist(bins=20)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")

            filename = f"{uuid.uuid4()}_{col}.png"
            filepath = os.path.join(PLOT_DIR, filename)
            plt.savefig(filepath)
            plt.close()
            plot_paths.append(f"/api/plots/{filename}")

        print("[VisualizationHandler] Generated histograms for numeric columns.")
        return {"plots": plot_paths}



