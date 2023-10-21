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

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    
    if not file or file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    # Upload to Google Cloud Storage
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    
    # Save metadata to Firestore
    doc_ref = db.collection('images').document(file.filename)
    doc_ref.set({
        'filename': file.filename,
        'content_type': file.content_type,
        'uploaded': firestore.SERVER_TIMESTAMP
    })
    
    return redirect('/')

def list_files():
    # Retrieve image metadata from Firestore
    images = db.collection('images').stream()
    
    files = []
    for image in images:
        files.append(image.to_dict())
    
    return files

@app.route('/list', methods=['GET'])
def list_images():
    return jsonify(list_files())

@app.route('/', methods=['GET'])
def index():
    images = list_files()
    image_elements = ""
    for image in images:
        image_elements += '<div class="col-lg-3 col-md-4 col-sm-6 col-12 mt-4"><div class="card"><a href="https://storage.googleapis.com/image-upload-bucket4/{}" download><img src="https://storage.googleapis.com/image-upload-bucket4/{}" alt="{}" class="img-fluid card-img-top"></a><div class="card-body"><h5 class="card-title">{}</h5></div></div></div>'.format(image["filename"], image["filename"], image["filename"], image["filename"])
    return html_string.format(image_elements)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


# HTML content integrated within the Python script
html_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="background-color: blue;">

<div class="container mt-5">
    <div class="text-center mb-5">
        <h2 class="display-4">Image Uploader (Serverless)</h2>
        <p class="lead">Project 2</p>
    </div>
    
    <!-- Upload Form -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">Upload an Image</div>
        <div class="card-body">
            <form action="/upload" method="post" enctype="multipart/form-data" class="d-flex flex-column align-items-center">
                <input type="file" name="file" accept="image/*" required class="mb-3">
                <button type="submit" class="btn btn-success">Upload</button>
            </form>
        </div>
    </div>
    
    <!-- Uploaded Images Grid -->
    <h3 class="mb-3">Uploaded Images</h3>
    <div class="row">
        {}
    </div>
    <br><br>
</div>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""
