import pandas as pd
from sklearn.pipeline import Pipeline as skPipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
import joblib
import motor.motor_asyncio
import os
import datetime
from db_models.pipeline_db_model import Pipeline

def train_pipeline( ml_models, client):

    pipeline= ml_models["ao_predictor"]
    print("Training model...")
    db = client["automl"]
    collection = db["data_set"]
    cursor = collection.find()
    data = list(cursor)
    # to convert data to pandas dataframe
    df = pd.DataFrame(data)

    # Split data into features (X) and target (y)
    X = df.drop("open_account_flg", axis=1)
    y = df["open_account_flg"]
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # Model Training and Evaluation using the pipeline
    pipeline.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, pipeline.predict(X_test))


    version = "init"
    #get the active pipeline
    active_pipeline = db["pipeline"].find_one({"active": True})
    if active_pipeline:
        #deactivate the active pipeline
        db["pipeline"].update_one({"active": True}, {"$set": {"active": False}})
        version = active_pipeline["version"]
        if version == "init":
            version = "1.0"
        else:
            version = str(round(float(version) + 1, 2))
    #save the new pipeline
    joblib.dump(pipeline, f"train/models/alif_aop_RF_pipeline_v{version}.pkl")
    pipeline= Pipeline(
        algorithm="RandomForest",
        name=f"alif_aop_RF_pipeline_v{version}.pkl",
        accuracy=accuracy,
        version=version,
        active=True,
        pipeline_path=f"train/models/alif_aop_RF_pipeline_v{version}.pkl",
        created_at= datetime.datetime.now(),
        updated_at= datetime.datetime.now(),
    )
    print("Model trained successfully!")
    result = db["pipeline"].insert_one(pipeline.dict())

    print("Loading newly trained pipeline...")
    ml_models["ao_predictor"] = joblib.load(f"train/models/alif_aop_RF_pipeline_v{version}.pkl")
    print("New pipeline loaded successfully!")




    return pipeline

