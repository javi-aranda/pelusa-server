from pydantic import BaseModel


class PredictionCreate(BaseModel):
    input: str


class Prediction(PredictionCreate):
    id: int
    features: str
    prediction: bool

    class Config:
        orm_mode = True


class PredictionResponse(BaseModel):
    prediction: bool

    class Config:
        orm_mode = True


class BulkPredictionResponse(BaseModel):
    input: str
    prediction: bool

    class Config:
        orm_mode = True
