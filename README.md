# FastAPI CRUD Operations

This project demonstrates a simple CRUD (Create, Read, Update, Delete) API using FastAPI framework. 

The Create (Post) method handles the creation of a user's profile. This method stores the user's basic information in the users table within MySQL, their addresses in the Addresses collection within MongoDB, and their favorite cuisine details in the Cuisine collection.

The Get method retrieves the user's preferred cuisine data.

The Put method enables users to update or modify their registered details (excluding the phone number). When users make changes, the updated data is stored in both databases, allowing them to view the updated information.

Lastly, the Delete method provides users with the option to remove their profile from the system, deleting all associated details.

## Setup

1. Clone the repository:
   git clone https://github.com/your-username/Recipes_Scraper
   cd fastapi-crud-api

2. Install dependencies
   pip install -r requirements.txt

3. Run the FastAPi server
   uvicorn main:app --reload


## Project Structure

- main.py                        # FastAPI code which contains the actual codes for POST,GET,PUT, DELETE
- data_clean.py                  # This code will replace all the empty values with Quantile range in the 'Prep Time'
- data_clean_add_time.py         # This code will add both Prep Time and Cook Time keys wherever the Total Time key has empty 
- README.md                      # Project documentation
- requirements.txt               # List of project dependencies