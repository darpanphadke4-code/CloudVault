from flask import Flask
from config import Config
from services.azure_blob import get_blob_service

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    try:
        blob_service = get_blob_service()

        containers = list(blob_service.list_containers())

        print("✅ Connected to Azure!")

        print("\nContainers:")

        for container in containers:
            print("-", container["name"])

    except Exception as e:
        print("❌ Connection Failed")
        print(e)