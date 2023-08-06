from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
import uvicorn
from schema import PredictionInputBase, DataEntryBase
import motor.motor_asyncio
import os
from fastapi.params import Depends
from db_models.data_db_model import Data
from starlette.background import BackgroundTasks
from train.train_pipeline import train_pipeline
from db_models.db_client import get_mongo_db
from db_models.pipeline_db_model import Pipeline
import datetime

UPDATE_INTERVAL_SECONDS = 3600  # Update every hour

# Placeholder for current model
current_model = None
last_update_time = 0
mongo_client = None
ml_models = {}


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)
@app.on_event('startup')
async def startup_event():
    global mongo_client
    mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    # Load the ML model
    #get the active pipeline
    db = mongodb_client["automl"]
    active_pipeline = await db["pipeline"].find_one({"active": True})
    if not active_pipeline:
        ml_models["ao_predictor"] = joblib.load('train/models/alif_aop_RF_pipeline_init.pkl')
        pipeline= Pipeline(
            algorithm="RandomForest",
            name="alif_aop_RF_pipeline_init.pkl",
            accuracy=0.8,
            version="1.0",
            active=True,
            pipeline_path="train/models/alif_aop_RF_pipeline_init.pkl",
            created_at= datetime.datetime.now(),
            updated_at= datetime.datetime.now(),
        )
        ml_models["ao_predictor_tmp"] = joblib.load(pipeline.pipeline_path)

        db = mongodb_client["automl"]
        result = db["pipeline"].insert_one(pipeline.dict())
        print("Loading initial pipeline")
    else:
        ml_models["ao_predictor"] = joblib.load(active_pipeline["pipeline_path"])
        print("Loading active pipeline")
    #Load the ML metadata
@app.on_event('shutdown')
async def shutdown_event():
    ml_models["ao_predictor"] = None
@app.get("/")
async def homepage():
    return {"message": "Welcome to AutoML FastAPI application."}
@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(title="AutoML FastAPI Application.",
                    description="This application serves an AutoML model for credit account prediction.\n"
                                "Features: \n"
                                "1. A new machine learning pipeline is created and trained every hour. \n"
                                "2. The latest trained pipeline is served for predictions. \n "
                    ,
                    version="1", routes=app.routes)
    )
    return response


@app.get("/docs", tags=["documentation"])
async def get_documentation():
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    return response
@app.post("/add_data")
async def add_data(data: Data, BackgroundTasks: BackgroundTasks, client=Depends(get_mongo_db)):
        """
        Add new data for training.

        - **data**: Data to be added for training.

        Returns:
        - **id**: ID of the inserted data.
        """
        data = Data(**data.dict())
        db = client["automl"]
        result = db["data_set"].insert_one(data.dict())
        global last_update_time, UPDATE_INTERVAL_SECONDS
        if last_update_time + UPDATE_INTERVAL_SECONDS < datetime.datetime.now().timestamp():
            last_update_time = datetime.datetime.now().timestamp()
            BackgroundTasks.add_task(train_pipeline, ml_models, client)

        return {"id": str(result.inserted_id)}



@app.post("/predict")
def predict(data: PredictionInputBase, client=Depends(get_mongo_db)):
    """
        Make predictions based on input data.

        - **data**: Input data for prediction.

        Returns:
        - **result**: Prediction result (0 or 1) indicating whether the client will open a credit account.
        - **confidence**: Confidence level of the prediction.
        - **model**: Active model details.
    """
    input_data = pd.DataFrame([data.dict()])
    try:
        result = ml_models["ao_predictor"].predict(input_data).tolist()[0]
        confidence = ml_models["ao_predictor"].predict_proba(input_data).tolist()[0][result]
        model= client["automl"]["pipeline"].find_one({"active": True},{"_id":0})
    except Exception as e:
        try:
            result = ml_models["ao_predictor_tmp"].predict(input_data).tolist()[0]
            confidence = ml_models["ao_predictor_tmp"].predict_proba(input_data).tolist()[0][result]
            model= client["automl"]["pipeline"].find_one({"active": True},{"_id":0})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail="Model is not ready yet.")
    return {"result": result,
            "confidence": confidence,
            "model": model}