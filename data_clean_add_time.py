import pandas as pd
import json

# Load the JSON file into a pandas DataFrame
with open('updated_mushroom_recipes.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Access the "recipe data" from the JSON
recipe_data = data.get('recipe data', [])

df = pd.DataFrame(recipe_data)

# Print out the column names to check for the correct column name
print("Original Column Names:", df.columns)

# Convert column names to lowercase and remove spaces
df.columns = df.columns.str.lower().str.replace(' ', '')

# Print out the updated column names
print("Updated Column Names:", df.columns)

# Define a function to convert time strings to minutes
def convert_to_minutes(time_str):
    if time_str == "":
        return 0
    # Remove " minutes" from the string and convert to integer
    return int(time_str.replace(" minutes", ""))

# Convert "preptime" and "cooktime" columns to minutes
df['preptime'] = df['preptime'].apply(convert_to_minutes)
df['cooktime'] = df['cooktime'].apply(convert_to_minutes)

# Update "cooktime" for recipes with missing values
df['cooktime'] = df.apply(lambda row: row['preptime'] if row['cooktime'] == 0 else row['cooktime'], axis=1)

# Calculate "totaltime" by adding "preptime" and "cooktime" (in minutes)
df['totaltime'] = df['preptime'] + df['cooktime']

# Convert "preptime", "cooktime", and "totaltime" back to string format with " minutes"
df['preptime'] = df['preptime'].astype(str) + " minutes"
df['cooktime'] = df['cooktime'].astype(str) + " minutes"
df['totaltime'] = df['totaltime'].astype(str) + " minutes"

# Convert DataFrame back to JSON format
updated_data = df.to_dict(orient='records')

# Create the updated JSON structure
updated_json = {
    "code": data.get("code", None),
    "message": data.get("message", None),
    "status": data.get("status", None),
    "recipe data": updated_data
}

# Write the updated JSON back to file with ensure_ascii=False
with open('updated_mushroom_recipes_1.json', 'w', encoding='utf-8') as file:
    json.dump(updated_json, file, indent=4, ensure_ascii=False)
