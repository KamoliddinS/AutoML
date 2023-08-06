from pydantic import BaseModel, Field, EmailStr
from db_models.utils import PyObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

class Data(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    client_id: int = Field(...)
    gender: str = Field(...)
    age: int = Field(...)
    marital_status: str = Field(...)
    job_position: str = Field(...)
    credit_sum: float = Field(...)
    credit_month: int = Field(...)
    tariff_id: float = Field(...)
    score_shk: float = Field(...)
    education: str = Field(...)
    living_region: str = Field(...)
    monthly_income: float = Field(...)
    credit_count: int = Field(...)
    overdue_credit_count: int = Field(...)
    open_account_flg: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_id": 1,
                "gender": "F",
                "age": 48,
                "marital_status": "MAR",
                "job_position": "BIS",
                "credit_sum": 59998,
                "credit_month": 10,
                "tariff_id": 1.6,
                "score_shk": 0.421599,
                "education": "GRD",
                "living_region": "ЛЕНИНГРАДСКАЯ ОБЛАСТЬ",
                "monthly_income": 30000,
                "credit_count": 1,
                "overdue_credit_count": 0,
                "open_account_flg": 1,
            }
        }

