import pandas as pd
import numpy as np
from typing import Any

def to_native(value: Any) -> Any:
    """Recursively convert pandas / numpy objects to JSON-serializable native Python types."""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    if hasattr(value, 'item') and callable(getattr(value, 'item')):
        try:
            return to_native(value.item())
        except Exception:
            pass
    if isinstance(value, dict):
        return {str(k): to_native(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_native(v) for v in value]
    if isinstance(value, tuple):
        return tuple(to_native(v) for v in value)
    return value
