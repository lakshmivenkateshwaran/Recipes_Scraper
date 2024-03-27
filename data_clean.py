import pandas as pd
import json
import re

# Load the JSON file into a pandas DataFrame
with open('final_mushroom_recipes copy 2.json', 'r') as file:
    data = json.load(file)

# Access the "recipe data" from the JSON
recipe_data = data.get('recipe_data', [])

df = pd.DataFrame(recipe_data)

# Print out the column names to check for the correct column name
print("Column Names:", df.columns)

# Extract numeric part from "Prep Time" and convert to numeric
prep_time_column_name = 'Prep Time'  # Update with the correct column name
if prep_time_column_name in df.columns:
    df[prep_time_column_name] = df[prep_time_column_name].str.extract('(\d+)').astype(float)

    # Calculate quantiles, ignoring NaN values
    quantiles = df[prep_time_column_name].quantile([0.25, 0.5, 0.75])

    # Define a function to fill empty values with quantiles and round to whole number
    def fill_with_quantile(value):
        if pd.isnull(value):
            return round(quantiles[0.5])  # Fill with rounded median if NaN
        return round(value)

    # Apply the function to the "Prep Time" column
    df[prep_time_column_name] = df[prep_time_column_name].apply(fill_with_quantile)

    # Add "minutes" to the "Prep Time" values
    df[prep_time_column_name] = df[prep_time_column_name].astype(str) + " minutes"

    # Convert DataFrame back to JSON format
    updated_data = df.to_dict(orient='records')

    # Create the updated JSON structure
    updated_json = {
        "code": data.get("code", None),
        "message": data.get("message", None),
        "status": data.get("status", None),
        "recipe data": updated_data
    }

    # Write the updated JSON back to file
    with open('updated_mushroom_recipes.json', 'w') as file:
        json.dump(updated_json, file, indent=4, ensure_ascii=False)
else:
    print(f"Column '{prep_time_column_name}' not found in DataFrame.")
