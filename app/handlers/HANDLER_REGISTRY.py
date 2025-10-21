from app.handlers.cleaning import CleaningHandler
from app.handlers.summary import SummaryHandler
from app.handlers.visualization import VisualizationHandler
from typing import Dict, Type

HANDLER_REGISTRY: Dict[str, Type] = {
    "cleaning": CleaningHandler,
    "summary": SummaryHandler,
    "visualization": VisualizationHandler,
}