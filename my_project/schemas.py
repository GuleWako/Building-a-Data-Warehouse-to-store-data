from pydantic import BaseModel

class DetectedImage(BaseModel):
    id: int
    image: str
    class_: float
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float

class DetectedImageCreate(BaseModel):
    image: str
    class_: float
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float
