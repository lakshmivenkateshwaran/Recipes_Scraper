import json
import pandas as pd
import pymongo

# Read the JSON file into a pandas DataFrame
df = pd.read_json(r"C:\Users\venki\Work\scrapy_data_project_app\myproject\myproject\final_snacks_recipes copy.json")


# Get the number of rows (objects) in the DataFrame
mongo_uri = "mongodb://localhost:27017/"
db_name = "South_Indian_Recipes"
collection_name = "Recipes"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Convert DataFrame to list of dictionaries (each row as a dictionary)
data = df.to_dict(orient='records')

# Insert the data into the MongoDB collection
collection.insert_many(data)

# Print success message
print("Inserted", len(data), "documents into MongoDB")

# Close the MongoDB connection
client.close()



