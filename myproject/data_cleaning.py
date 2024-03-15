import json
import pandas as pd

# Read the JSON file into a pandas DataFrame
df = pd.read_json(r"C:\Users\venki\Work\scrapy_data_project_app\myproject\final_recipes.json")


if 'receipe_data' in df.columns:
    # Define the condition to check for empty values for all keys except "Title" and "Description"
    def is_empty_record(record):
        keys_to_check = ['Ingredients', 'Instructions', 'Prep Time', 'Cook Time', 'Total Time', 'Cuisine', 'Course']
        # Check if all keys except "Title" and "Description" have empty values
        return all((key not in record or key in ['Title', 'Description'] or
                    (isinstance(record[key], list) and len(record[key]) == 0) or
                    (isinstance(record[key], str) and not record[key].strip())) for key in keys_to_check)

    # Filter records based on the condition
    empty_records = df.loc[df['receipe_data'].apply(is_empty_record)]

    # Drop the rows with empty values for all specified keys
    df.drop(empty_records.index, inplace=True)

    # Convert the DataFrame to a list of dictionaries
    updated_records = df['receipe_data'].tolist()

    # Add new key-value pair 'Country': 'India' to each dictionary
    for record in updated_records:
        cuisine = record.get('Cuisine', '').lower()
        if 'tamil nadu' in cuisine:
            record['State'] = 'Tamilnadu'
        elif 'karnataka' in cuisine:
            record['State'] = 'Karnataka'
        elif 'kerala' in cuisine:
            record['State'] = 'Kerala'
        elif 'andhra' in cuisine or 'hyderabadi' in cuisine:
            record['State'] = 'Andhra Pradesh'
        else:
            # Default state if cuisine doesn't match
            record['State'] = 'Other'
        record['Country'] = 'India'

    json_data = {
            "code": 200,
            "status": "Success",
            "Message": "Successfully Fetched the Receipes List",
            "receipe_data": updated_records
        }
    # Save the updated records to a new JSON file with original formatting
    with open(r"C:\Users\venki\Work\scrapy_data_project_app\myproject\updated_final_recipes.json", 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print("Updated JSON file saved to 'updated_final_recipes.json'.")
else:
    print("'receipe_data' column not found in the DataFrame.")
