from typing import Callable

import numpy as np

from app.models.prediction import Prediction


async def test_prediction_model(create_prediction: Callable) -> None:
    prediction = await create_prediction("https://example.com", 1)
    prediction.set_features(np.array([1, 2, 3]))
    assert np.array_equal(prediction.get_features(), np.array([1, 2, 3]))
