import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "cloudvault-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "cloudvault.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AZURE_STORAGE_CONNECTION_STRING = os.getenv(
        "AZURE_STORAGE_CONNECTION_STRING"
    )

    AZURE_CONTAINER_NAME = os.getenv(
        "AZURE_CONTAINER_NAME"
    )