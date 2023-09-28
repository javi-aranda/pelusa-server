from pydantic import BaseModel


class CurrentTimeHealthy(BaseModel):
    ct: str
    msg: str
