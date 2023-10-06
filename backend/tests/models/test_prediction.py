import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction import Prediction


async def test_prediction_model(db: AsyncSession):
    prediction = Prediction(
        id=1,
        input="https://example.com",
        features="[1, 2, 3]",
        prediction=False,
    )
    db.add(prediction)
    await db.commit()
    assert prediction.id
    assert prediction.get_features() == np.array([1, 2, 3])
