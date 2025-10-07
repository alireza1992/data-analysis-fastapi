from handlers.cleaning import CleaningHandler
from handlers.summary import SummaryHandler
from handlers.visualization import VisualizationHandler

HANDLER_REGISTRY = {
    "cleaning": CleaningHandler,
    "summary": SummaryHandler,
    "visualization": VisualizationHandler,
}