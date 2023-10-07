from typing import Tuple

import numpy as np

from app.core.config import pelusa_model
from app.core.logger import logger
from app.ml.features.analyzer import StaticURLAnalyzer
from app.ml.features.top_features import get_available_features


async def analyze_url(input: str) -> Tuple[np.array, bool] | None:
    available_features = get_available_features()
    try:
        analyzer = StaticURLAnalyzer(input)
        features = analyzer.extract_info()
        features = {k: v for k, v in features.items() if k in available_features}
        features_array = np.array([list(features.values())]).reshape(1, -1)

        prediction = pelusa_model.predict(features_array)[0]
        return features_array, prediction
    except Exception as e:
        logger.exception(e)
