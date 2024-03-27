from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pymongo import MongoClient
import uvicorn
import re
import traceback
import bcrypt

# FastAPI App
app = FastAPI()

# SQLAlchemy Models
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost/planyourmeal"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    password = Column(String)
    gender = Column(String)
    language = Column(String)

# MongoDB Connection
MONGO_CONNECTION_URL = "mongodb://localhost:27017/"
mongo_client = MongoClient(MONGO_CONNECTION_URL)
mongo_db = mongo_client["planyourmeal"]
address_collection = mongo_db["addresses"]
cuisine_collection = mongo_db["cuisines"]
recipes_collection = mongo_client["South_Indian_Recipes"]["Recipes"]

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    phone_number: str
    password: str
    gender: str
    language: str
    country: str
    state: str
    district: str
    fav_cuisine_1: str
    fav_cuisine_2: str
    fav_cuisine_3: str

class UserUpdate(BaseModel):
    name: str = None
    age: int = None
    email: str = None
    password: str = None
    gender: str = None
    language: str = None
    country: str = None
    state: str = None
    district: str = None
    fav_cuisine_1: str = None
    fav_cuisine_2: str = None
    fav_cuisine_3: str = None

# FastAPI Endpoints
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate):
    try:
        db = SessionLocal()

        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        print("Creating user in MySQL...")
        db_user = User(
            name=user.name,
            age=user.age,
            email=user.email,
            phone_number=user.phone_number,
            password=hashed_password.decode('utf-8'),
            gender=user.gender,
            language=user.language,
        )
        print("Adding user to session...")
        db.add(db_user)
        print("Committing session...")
        db.commit()

        address_data = {
            "phone_number": user.phone_number,
            "country": user.country,
            "state": user.state,
            "district": user.district,
        }
        address_collection.insert_one(address_data)

        cuisine_data = {
            "phone_number": user.phone_number,
            "cuisines": [user.fav_cuisine_1, user.fav_cuisine_2, user.fav_cuisine_3]
        }
        cuisine_collection.insert_one(cuisine_data)

        db.close()
        print("User created successfully.")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# FastAPI Endpoint to Fetch Recipes
@app.get("/users/{phone_number}/recipes/")
def get_user_recipes(phone_number: str):
    try:
        # Fetch user's favorite cuisines from MongoDB
        user_cuisines = cuisine_collection.find_one({"phone_number": phone_number})
        if not user_cuisines:
            raise HTTPException(status_code=404, detail="User not found")

        # Extract favorite cuisines
        fav_cuisines = user_cuisines.get("cuisines", [])

        # Create a filter for the recipes
        regex_patterns = [
            re.compile(r"\b" + re.escape(cuisine) + r"\b", re.IGNORECASE) for cuisine in fav_cuisines
        ]
        filter_query = {
            "$or": [
                {"Cuisine": {"$in": fav_cuisines}},
                {"Cuisine": {"$regex": "|".join(pattern.pattern for pattern in regex_patterns)}}
            ]
        }

        # MongoDB query to fetch recipes based on user's favorite cuisines
        user_recipes = recipes_collection.find(filter_query, {"_id": 0})
        recipes_list = list(user_recipes)

        if not recipes_list:
            raise HTTPException(status_code=404, detail="No recipes found for the user's favorite cuisines")

        return recipes_list

    except Exception as e:
        # Log the error
        print(f"Error in fetching recipes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
# FastAPI Endpoint to Update User Details
@app.put("/users/{phone_number}/update/", response_model=UserUpdate)
def update_user(phone_number: str, user_update: UserUpdate):
    try:

        # Update user details in MySQL
        db = SessionLocal()
        db_user = db.query(User).filter(User.phone_number == phone_number).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update only the fields that are present in the request
        for field in user_update.dict(exclude_unset=True):
            if hasattr(user_update, field) and getattr(user_update, field) is not None:
                setattr(db_user, field, getattr(user_update, field))

        db.commit()
        db.refresh(db_user)
        db.close()

        # Update user details in MongoDB for addresses
        address_data = {
            "phone_number": phone_number,
            "country": user_update.country,
            "state": user_update.state,
            "district": user_update.district,
        }
        address_collection.update_one(
            {"phone_number": phone_number},
            {"$set": address_data},
            upsert=True
        )

        # Update user details in MongoDB for cuisines
        cuisine_data = {
            "phone_number": phone_number,
            "cuisines": [user_update.fav_cuisine_1, user_update.fav_cuisine_2, user_update.fav_cuisine_3]
        }
        cuisine_collection.update_one(
            {"phone_number": phone_number},
            {"$set": cuisine_data},
            upsert=True
        )

        return user_update

    except HTTPException as e:
        # Log the error
        print(f"HTTP Exception: {e.status_code} - {e.detail}")
        raise e

    except Exception as e:
        # Log the error with traceback
        import traceback
        traceback.print_exc()
        print(f"Error in updating user details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# FastAPI Endpoint to Delete User
@app.delete("/users/{phone_number}/delete/", response_model=dict)
def delete_user(phone_number: str):
    try:
        # Delete user from MySQL
        db = SessionLocal()
        db_user = db.query(User).filter(User.phone_number == phone_number).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(db_user)
        db.commit()
        db.close()

        # Delete user from MongoDB for addresses
        address_collection.delete_one({"phone_number": phone_number})

        # Delete user from MongoDB for cuisines
        cuisine_collection.delete_one({"phone_number": phone_number})

        return {"message": "User deleted successfully"}

    except HTTPException as e:
        # Log the error
        print(f"HTTP Exception: {e.status_code} - {e.detail}")
        raise e

    except Exception as e:
        # Log the error with traceback
        import traceback
        traceback.print_exc()
        print(f"Error in deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
