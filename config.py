from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class Config:
    MONGO_URI = f"mongodb+srv://ofeksimantov:{os.environ.get('MONGO_PWD')}@jobs.a0bxjop.mongodb.net/?retryWrites=true&w=majority"
