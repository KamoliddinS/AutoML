from pydantic import BaseModel, Field, EmailStr
from db_models.utils import PyObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class Pipeline(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    algorithm: str = Field(...)
    name: str = Field(...)
    accuracy: float = Field(...)
    version: str = Field(...)
    pipeline_path: str = Field(...)
    active: bool = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "algorithm": "RandomForest",
                "name": "alif_aop_RF_pipeline_v1.pkl",
                "accuracy": 0.9,
                "version": "1.0",
                "active": True,
                "pipeline_path": "train/models/alif_aop_RF_pipeline_v1.pkl",
            }
        }
