from pydantic import BaseModel

class PredictionInputBase(BaseModel):
    gender: str
    age: int
    marital_status: str
    job_position: str
    credit_sum: float
    credit_month: int
    tariff_id: float
    score_shk: float
    education: str
    living_region: str
    monthly_income: float
    credit_count: float
    overdue_credit_count: float

class DataEntryBase(PredictionInputBase):
    client_id: str
