from typing import Tuple
import numpy as np

from app.ml.features.analyzer import StaticURLAnalyzer
from app.core.config import pelusa_model
from app.core.logger import logger


def get_available_features():
    return np.array(
        [
            'url_fragments', 'excessive_subdomains', 'numeric_domain',
            'domain_length', 'path_length', 'percent_chars', 'at_chars',
            'dash_chars', 'question_chars', 'and_chars', 'equal_chars',
            'underscore_chars', 'shannon_entropy', 'suspicious_keywords',
            'shortened_url',
        ]
    )

async def analyze_url(input: str) -> Tuple[np.array, bool]:
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
