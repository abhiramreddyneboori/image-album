import os
import logging
from flask import Flask, request, jsonify, redirect
from google.cloud import storage, firestore

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Firestore
db = firestore.Client()

# Initialize Cloud Storage
storage_client = storage.Client()
bucket_name = 'image-upload-bucket4'
bucket = storage_client.bucket(bucket_name)

# Rest of your existing code...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
