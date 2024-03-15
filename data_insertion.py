import pymongo
import json
from myproject import data_cleaning as dc

updated_records = dc.updated_records

# Define the function to store records to MongoDB
def store_to_mongo(records):
    # Define the MongoDB connection details
    mongo_uri = "mongodb://localhost:27017/"
    db_name = "South_Indian_Recipes"
    collection_name = "Recipes"

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Insert the records into MongoDB
    result = collection.insert_many(records)
    print("Inserted", len(result.inserted_ids), "documents into MongoDB")

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    # Call the store_to_mongo function
    store_to_mongo(updated_records)

