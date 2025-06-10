import os
import cloudinary
import cloudinary.uploader
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")

# MongoDB config
client = MongoClient(os.getenv("MONGO_URI"))
db = client["preparation"]  # Change as needed
collection = db["songs"]  # Same name as your MERN app collection

# Path to your local images
image_dir = os.path.join(os.getcwd(), "images", "pre-catechumenate")

# Upload each image and insert record
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        image_path = os.path.join(image_dir, filename)

        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(image_path, folder="neo_catechumenate_songs")

            # Extract data
            public_id = upload_result["public_id"]
            secure_url = upload_result["secure_url"]

            # Create DB record
            song_doc = {
                "title": os.path.splitext(filename)[0].replace('_', ' ').title(),
                "imageUrl": secure_url,
                "description": "",  # Add if you have description logic
                "category": "pre-catechumenate",  # Adjust as needed
            }

            # Insert to MongoDB
            result = collection.insert_one(song_doc)
            print(f"Uploaded & inserted: {filename} → MongoID: {result.inserted_id}")

        except Exception as e:
            print(f"Error uploading {filename}: {str(e)}")
