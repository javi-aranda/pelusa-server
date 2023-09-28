import json
from datetime import datetime

import numpy as np
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime

from app.db import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    input: Mapped[str | None]
    features: Mapped[str | None]
    prediction: Mapped[bool | None]
    validated_prediction: Mapped[bool | None]
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def set_features(self, features_array):
        self.features = json.dumps(features_array.tolist())

    def get_features(self):
        return np.array(json.loads(self.features))
