import csv
from pymongo import MongoClient
from pydantic import BaseModel, Field
from bson import ObjectId
import pandas as pd
import os
from db_models.utils import PyObjectId
from db_models.data_db_model import Data


def populate_mongodb_from_csv(csv_file, db_name, collection_name, mongo_uri=os.environ["MONGODB_URL"]):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Load CSV data into a pandas DataFrame
    df = pd.read_csv(csv_file)
    df.dropna(inplace=True)


    def convert_credit_sum(value):
        try:
            return float(value.replace(',', '.'))
        except:
            return 0

    # Convert incorrect data types to numerical
    df['credit_sum'] = df['credit_sum'].apply(convert_credit_sum)
    df['score_shk'] = df['score_shk'].str.replace(',', '.').astype(float)
    # Iterate through the DataFrame and insert/update documents in the MongoDB collection
    for _, row in df.iterrows():
        client_id = int(row['client_id'])
        existing_doc = collection.find_one({'client_id': client_id})

        if existing_doc:
            # Update existing document
            updated_doc = Data(
                id=existing_doc['_id'],  # Preserve existing ObjectId
                **row.to_dict()  # Convert Series to dictionary
            )
            collection.update_one({'_id': existing_doc['_id']}, {'$set': updated_doc.dict()})
        else:
            # Insert new document
            new_doc = Data(**row.to_dict())
            collection.insert_one(new_doc.dict())

    client.close()

# Usage example
csv_file_path = os.environ["CSV_FILE_PATH"]
db_name = 'automl'
collection_name = 'data_set'

populate_mongodb_from_csv(csv_file_path, db_name, collection_name)